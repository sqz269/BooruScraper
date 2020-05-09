from itertools import dropwhile
from collections import Counter
import parse
import os

def write_frequent_tags(output_file, data: Counter):
    with open(output_file, "wb") as file:
        file.write("tag_name,tag_count\n".encode("utf-8"))
        for entry in data.most_common():
            file.write("{}, {}\n".format(entry[0], entry[1]).encode("utf-8"))

def find_most_frequent_tags(src_csv: str, dst_csv: str, thresh_hold, delimiter, tags_column_name):
    write_frequent_tags(dst_csv, get_most_frequent_tags(src_csv, thresh_hold, delimiter, tags_column_name))

def get_most_frequent_tags(src_csv: str, thresh_hold=5, delimiter=",", tags_column_name="image_tags"):
    """
    Get most frequent tags from scraped data
    """
    tags_string = ""
    # String that stores every tag with a space that is separating them
    # with repeated tags. Ex: it's content might be "1girl skirts 1girl 1girl"

    with open(src_csv, "r") as file:
        headers = file.readline().strip().split(delimiter) # Assume first line is the header and extract it
        headers = [i.strip() for i in headers]
        tags_column = headers.index(tags_column_name)
        for lines in file:
                         # First remove start end spaces then split them using the delimiter
                         # and finally get the tags columns
            tags_string += lines.strip().split(delimiter)[tags_column].strip() + " "  # Add a space to the end to separate it from next line

        tags_count = Counter(tags_string.split(" "))

        # Delete any keys that their occurrence if lower than the thresh hold
        for key, count in dropwhile(lambda key_count: key_count[1] >= thresh_hold, tags_count.most_common()):
            del tags_count[key]

    return tags_count

def find_diff_all_delete(src_csv: str, files_dir: str, output_csv: str, file_format_string: str, thresh_hold=3, delimiter=",", post_format_unique_identifier="post_id"):
    """
    Get the files have been deleted, and compare it from the total tags and deleted tags
    Unlike find_diff_remain_del this function only compares the total tags and deleted

    Arguments:
        src_csv {string (path-like)} -- the csv that stores tag information about every file that was in the files_dir
        files_dir {string (path-like)} -- the directory that stores all the files that has been scraped (or the ones that didn't get deleted)
        output_csv {string (path-like)} -- the path to write the output of the difference to
        file_format_string {string} -- the format string used to formulate the file name (such as: "{image_id}-{image_likes}-{image_index}.jpg")

    Keyword Arguments:
        thresh_hold {int} -- the number of occurrences of the tag in order for it to be take account into the difference and write in output csv (default: {3})
        delimiter {str} -- the original csv's delimiter (default: {","})
    """
    csv_data = []
    with open(src_csv, "r") as file:
        headers = file.readline().strip().split(delimiter)
        for lines in file:
            csv_data.append(lines.strip().split(delimiter))


    post_id_remain = []
    for (directory, _, filename) in os.walk(files_dir): # Walk the direction that stores remaining of the files (files after uses has deleted the one they didn't like)
        for file in filename:
            post_id = parse.parse(file_format_string, file)[post_format_unique_identifier]
            # Reverse the formatting of the file name and get the Identifier for each picture
            post_id_remain.append(post_id)


    post_entry_removed = []
    for post_data in csv_data:
        if post_data[0] not in post_id_remain:
            post_entry_removed.append(post_data)


    post_entry_removed_tags_string = ""
    # String that stores the list of tags that been removed, it will be counter later
    for data in post_entry_removed:
        post_entry_removed_tags_string += data[headers.index("tags")] + " "

    post_entry_removed_tags_counter = Counter(post_entry_removed_tags_string.split(" "))  # use counter to store the tags removed

    post_entry_tags_counter = get_most_frequent_tags(src_csv, thresh_hold=thresh_hold, delimiter=delimiter)
    # get the total tags count
    tags_not_deleted = set(post_entry_tags_counter.keys()) - set(post_entry_removed_tags_counter.keys())
    # Subtract the total tags count with the removed tags count to get the ones that are not deleted

    # if none of that tag are deleted, they deleted count to be set to 0
    for tags in tags_not_deleted:
        post_entry_removed_tags_counter.update({tags: 0})

    post_entry_tags_counter = dict(sorted(post_entry_removed_tags_counter.items(),key = lambda i: i[0]))
    post_entry_tags_counter = dict(sorted(post_entry_tags_counter.items(),key = lambda i: i[0]))

    with open(output_csv, "w") as file:
        headers = "{tags},{tags_count},,,{deleted_tags},{deleted_tags_count}\n"  # CSV headers and corresponding data fields
        file.write(headers.replace("{", "").replace("}", ""))
        for (k, v), (k2, v2) in zip(post_entry_tags_counter.items(), post_entry_removed_tags_counter.items()):
        #   k = the tag name itself; v = the total occurrence of the tag; k2 = the deleted tags name; v2 = total times of the tag k2 has been deleted
            file.write(headers.format(tags=k, tags_count=v, deleted_tags=k2, deleted_tags_count=v2))

def find_diff_remain_del(src_csv, files_dir, output_csv, file_format_string, thresh_hold=3, delimiter=",", post_format_unique_identifier="post_id"):
    """Find the tags for comparesion between the deleted and the not deleted files

    Arguments:
        src_csv {string (path-like)} -- the csv that stores tag information about every file that was in the files_dir
        files_dir {string (path-like)} -- the directory that stores all the files that has been scraped (or the ones that didn't get deleted)
        output_csv {string (path-like)} -- the path to write the output of the difference to
        file_format_string {string} -- the format string used to formulate the file name (such as: "{image_id}-{image_likes}-{image_index}.jpg")

    Keyword Arguments:
        thresh_hold {int} -- the number of occurrences of the tag in order for it to be take account into the difference and write in output csv (default: {3})
        delimiter {str} -- the original csv's delimiter (default: {","})
    """
    csv_data = []
    with open(src_csv, "r") as file:
        headers = file.readline().strip().split(delimiter)
        for lines in file:
            csv_data.append(lines.strip().split(delimiter))


    post_id_remain = []
    counter = 0
    for (directory, _, filename) in os.walk(files_dir):
        for file in filename:
            post_id = parse.parse(file_format_string, file)[post_format_unique_identifier]  # use reverse format to find the post_id
            post_id_remain.append(post_id)

    post_entry_remain = []
    post_entry_removed = []
    for post_data in csv_data:  # Determin which post has been deleted by the user
        if post_data[0] in post_id_remain:
            post_entry_remain.append(post_data)
        else:
            post_entry_removed.append(post_data)

    post_entry_remain_tags_string = ""
    for data in post_entry_remain:  # Determin the tags of the post that the user didn't delete
        post_entry_remain_tags_string += data[headers.index("tags")] + " "

    post_entry_removed_tags_string = ""
    for data in post_entry_removed:  # Determin the tags of the post the user deleted
        post_entry_removed_tags_string += data[headers.index("tags")] + " "

    post_entry_tag_remain_counter = Counter(post_entry_remain_tags_string.split(" "))  # Count the tags and store it in a counter which have the {<TagName>: <RemainingCount>}
    for key, count in dropwhile(lambda key_count: key_count[1] >= thresh_hold, post_entry_tag_remain_counter.most_common()):
        # Loop though the keys and remove the tags that have little occurrences (that have occurrences less than the threshold amt)
        del post_entry_tag_remain_counter[key]

    post_entry_tag_removed_counter = Counter(post_entry_removed_tags_string.split(" "))  # {<TagName>: <DeletedCount>}
    for key, count in dropwhile(lambda key_count: key_count[1] >= thresh_hold, post_entry_tag_removed_counter.most_common()):
        # Loop though the keys and remove the tags that have little occurrences (that have occurrences less than the threshold amt)
        del post_entry_tag_removed_counter[key]

    with open(output_csv, "w") as file:
        headers = "remain_tags, remain_tags_count\n"
        file.write(headers)
        for entry in post_entry_tag_remain_counter.most_common():
            # Write All the tags that is remaining to CSV
            file.write("{},{}\n".format(entry[0], entry[1]))

        file.write("\n\n\n\n")

        headers = "deleted_tags, deleted_tags_count\n"
        file.write(headers)
        for entry in post_entry_tag_removed_counter.most_common():
            file.write("{},{}\n".format(entry[0], entry[1]))

INT_TO_FUNCTION = {
    1: find_most_frequent_tags,
    2: find_diff_all_delete,
    3: find_diff_remain_del
}

def start():
    func = None
    while True:
        try:
            print("1) Find The Most Frequent Tags")
            print("2) Find Deleted Tags and Compare to All Existed Tags")
            print("3) Find Deleted Tags and Compare to Remaining Tags which didn't get deleted")
            func = int(input("Choose Function (1-3): "))
            if (func > 3 or func <= 0):
                raise TypeError()
            break
        except ValueError:
            print("Please Enter a valid Option (1-3): ")

    actual_function = INT_TO_FUNCTION[func]

    if func == 1:
        csv_path = input("Enter the path of the csv file: ")
        delimiter = input("Enter CSV delimiter (default \",\"): ") or ","
        out_csv = input("Enter the path for the output csv file: ")
        threshold = input("Enter threshhold (default \"5\"): ") or 5
        tags_column_name = input("Enter the name of the column contains tags: (default \"image_tags\"): ") or "image_tags"
        actual_function(csv_path, out_csv, int(threshold), delimiter, tags_column_name)
    else:
        csv_path = input("Enter the path of the csv file: ")
        f_dir = input("Enter the path to the directory that stores scraped images: ")
        o_csv = input("Enter output csv's path (including name): ")
        ff_str = input("Enter the file name format string (FILENAME_STRING in config): ")
        ff_id = input("Enter the unique identifier for each image (image_id): ")
        delimiter = input("Enter CSV delimiter (default \",\"): ") or ","
        threshold = input("Enter threshhold (default \"3\"): ") or 3
        args = [csv_path, f_dir, o_csv, ff_str, int(threshold), delimiter, ff_id]
        actual_function(*args)


if __name__ == "__main__":
    start()
