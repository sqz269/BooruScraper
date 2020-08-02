# TODO: REFACTOR OR SOMETHING LIKE THAT IDK

import os
from collections import Counter
from itertools import dropwhile

import parse


def write_frequent_tags(output_file, data: Counter):
    with open(output_file, "wb") as file:
        file.write("tag_name,tag_count\n".encode("utf-8"))
        for entry in data.most_common():
            file.write("{}, {}\n".format(entry[0], entry[1]).encode("utf-8"))


def find_most_frequent_tags(src_csv: str, dst_csv: str, threshold, delimiter, tags_column_name):
    write_frequent_tags(dst_csv, get_most_frequent_tags(src_csv, threshold, delimiter, tags_column_name))


def get_most_frequent_tags(src_csv: str, threshold=5, delimiter=",", tags_column_name="d"):
    """
    Get most frequent tags from scraped data
    """
    tags_string = ""
    # String that stores every tag with a space that is separating them
    # with repeated tags. Ex: it's content might be "1girl skirts 1girl 1girl"

    with open(src_csv, "r") as file:
        headers = file.readline().strip().split(delimiter)  # Assume first line is the header and extract it
        headers = [i.strip() for i in headers]
        tags_column = headers.index(tags_column_name)
        for lines in file:
            # First remove start end spaces then split them using the delimiter
            # and finally get the tags columns
            tags_string += lines.strip().split(delimiter)[
                               tags_column].strip() + " "  # Add a space to the end to separate it from next line
            # Concat all tags into one string not very effective

        tags_count = Counter(tags_string.split(" "))

        # Delete any keys that their occurrence if lower than the thresh hold
        for key, count in dropwhile(lambda key_count: key_count[1] >= threshold, tags_count.most_common()):
            del tags_count[key]

    return tags_count


def find_diff_del(src_csv, files_dir, output_csv, file_format_string, threshold, delimiter,
                  post_format_unique_identifier, tags_column_name):
    csv_data = []
    with open(src_csv, "r") as file:
        headers = file.readline().strip().split(delimiter)
        headers = [i.strip() for i in headers]
        for lines in file:
            csv_data.append(lines.strip().split(delimiter))

    post_id_remain = []
    for (directory, _, filename) in os.walk(files_dir):  # Walk the directory that stores remaining of the files
        for file in filename:
            # Reverse the formatting of the file name and get the Identifier for each picture
            post_id = parse.parse(file_format_string, file)[post_format_unique_identifier]
            post_id_remain.append(post_id)

    post_id_removed = []
    post_data_remain = []
    for post_data in csv_data:  # all the ones that is not in remaining files are assumed to be deleted
        if post_data[0] not in post_id_remain:
            post_id_removed.append(post_data)
        else:
            post_data_remain.append(post_data)
    post_id_remain = post_data_remain

    post_entry_remain_tags_string = ""
    for data in post_id_remain:
        post_entry_remain_tags_string += data[headers.index(tags_column_name)].strip() + " "

    post_entry_removed_tags_string = ""
    # String that stores the list of tags that been removed, it will be counter later
    for data in post_id_removed:
        post_entry_removed_tags_string += data[headers.index(tags_column_name)].strip() + " "

    post_all_tags_counter = get_most_frequent_tags(src_csv, threshold=threshold, delimiter=delimiter,
                                                   tags_column_name=tags_column_name)
    # get all of the tags within the threshold
    post_removed_tags_counter = Counter(
        post_entry_removed_tags_string.split(" "))  # use counter to store the tags removed
    post_remaining_tags_counter = Counter(
        post_entry_remain_tags_string.split(" "))  # use counter to store the tags remaining

    tags_not_deleted = set(post_all_tags_counter.keys()) - set(post_removed_tags_counter.keys())
    # Subtract the total tags count with the removed tags count to get the ones that are not deleted
    # if none of that tag are deleted, they deleted count to be set to 0
    for tags in tags_not_deleted:
        post_removed_tags_counter.update({tags: 0})

    tags_not_remaining = set(post_all_tags_counter.keys()) - set(post_remaining_tags_counter.keys())
    # Subtract the total tags count with the removed tags count to get the ones that are not deleted
    for tags in tags_not_remaining:
        post_remaining_tags_counter.update({tags: 0})

    # Remove that did not meet the threshold requirement
    # this will work because post_all_tags_counter have already removed any tags that is not with in the threshold
    tags_missing = set(post_remaining_tags_counter.keys()) - set(post_all_tags_counter.keys())
    for tags in tags_missing:
        del post_remaining_tags_counter[tags]

    tags_missing = set(post_removed_tags_counter.keys()) - set(post_all_tags_counter.keys())
    for tags in tags_missing:
        del post_removed_tags_counter[tags]

    post_removed_tags_counter = dict(sorted(post_removed_tags_counter.items(), key=lambda i: i[0]))
    post_remaining_tags_counter = dict(sorted(post_remaining_tags_counter.items(), key=lambda i: i[0]))
    post_all_tags_counter = dict(sorted(post_all_tags_counter.items(), key=lambda i: i[0]))

    csv_header = "{total_tag_name},{tag_count},,{removed_tag_name},{tag_count},,{remaining_tag_name},{tag_count}\n"
    with open(output_csv, "wb") as file:
        file.write(csv_header.replace("{", "").replace("}", "").encode("utf-8"))
        for (k, v), (k1, v1), (k2, v2) in zip(post_all_tags_counter.items(), post_removed_tags_counter.items(),
                                              post_remaining_tags_counter.items()):
            file.write(f"{k},{v},,{k1},{v1},,{k2},{v2}\n".encode("utf-8"))


def start():
    while True:
        try:
            print("1) Find The Most Frequent Tags")
            print("2) Find Deleted Tags and Compare")
            func = int(input("Choose Function (1-2): "))
            if func > 2 or func <= 0:
                raise TypeError()
            break
        except ValueError:
            print("Please Enter a valid Option (1-2): ")

    if func == 1:
        csv_path = input("Enter the path of the csv file: ")
        delimiter = input("Enter CSV delimiter (default \",\"): ") or ","
        out_csv = input("Enter the path for the output csv file: ")
        threshold = int(input("Enter threshhold (default \"5\"): ")) or 5
        tags_column_name = input(
            "Enter the name of the column contains tags: (default \"image_tags\"): ") or "image_tags"
        find_most_frequent_tags(csv_path, out_csv, int(threshold), delimiter, tags_column_name)
    else:
        csv_path = input("Enter the path of the csv file: ")
        f_dir = input("Enter the path to the directory that stores scraped images: ")
        o_csv = input("Enter output CSV's path (including name): ")
        ff_str = input("Enter the file name format string (FILENAME_STRING in config): ")
        ff_id = input("Enter the unique identifier for each image (default \"image_id\"): ") or "image_id"
        tags_column_name = input(
            "Enter the name of the column contains tags: (default \"image_tags\"): ") or "image_tags"
        delimiter = input("Enter CSV delimiter (default \",\"): ") or ","
        threshold = int(input("Enter threshhold (default \"3\"): ")) or 3
        args = [csv_path, f_dir, o_csv, ff_str, int(threshold), delimiter, ff_id, tags_column_name]
        find_diff_del(*args)


if __name__ == "__main__":
    start()
