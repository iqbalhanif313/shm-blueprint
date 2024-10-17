import asyncio
import os

# Define the folder containing the Python files
folder_path = '.'  # Replace 'scripts' with your target folder name

async def run_python_file(file_path):
    # Run the Python file using subprocess
    process = await asyncio.create_subprocess_exec(
        'python3', file_path,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    print(f"Running {file_path}")
    
    stdout, stderr = await process.communicate()
    
    if process.returncode == 0:
        print(f"Successfully ran {file_path}")
    else:
        print(f"Failed to run {file_path}. Error:\n{stderr.decode()}")

async def run_all_files_in_folder(folder):
    tasks = []
    # Loop through all files in the folder
    for filename in os.listdir(folder):
        if filename.endswith('.py') and filename != os.path.basename(__file__):
            file_path = os.path.join(folder, filename)
            tasks.append(run_python_file(file_path))
    
    # Run all Python files asynchronously
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(run_all_files_in_folder(folder_path))