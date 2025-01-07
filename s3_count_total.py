import os

def calculate_total_with_hierarchy(root_folder):
    """

    Script used to calculate the AWS DataSync quota using total count for files and directories where:
    - Each file contributes 1 + the number of folders in its hierarchy.

    Args:
        root_folder (str): The path to the root folder.

    Returns:
        int: The total count.
    """
    total_count = 0

    for root, dirs, files in os.walk(root_folder):
        # Get the current hierarchy depth (relative to the root folder)
        relative_depth = root[len(root_folder):].count(os.sep)

        # For each file, add 1 + hierarchy depth to the total count
        for file in files:
            total_count += 1 + relative_depth

    return total_count

if __name__ == "__main__":
    root_folder = input("Enter the path to the root folder: ").strip()

    if os.path.exists(root_folder):
        total_count = calculate_total_with_hierarchy(root_folder)
        if total_count > 25000000:
            print(f"AWS DataSync default quota exceeded")
        print(f"The count towards quota: {total_count}")
    else:
        print("The specified folder does not exist.")
