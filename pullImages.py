import subprocess
import sys
import argparse

def clone_repo(repo_name):
	# Clone the git repo
	try:
		print(f"\nCloning : {repo_name}\n")
		subprocess.run(['git', 'clone', f'{repo_name}'], check=True)
	except subprocess.CalledProcessError as e:
		print(f"Failed to clone the git repo {repo_name}. Error: {e}")
		print(f"\nUse the --skip-clone argument to skip cloning the repo again.")
		sys.exit()


def process_docker_images(input_file, output_file, local_registry):
	with open(input_file, 'r') as file:
		images = file.readlines()

	with open(output_file, 'w') as file:
		for image in images:
			image = image.strip()
			if not image:
				continue

			# Assuming the image name and tag are separated by a colon
			if ':' in image:
				image_name, tag = image.split(':')
			else:
				image_name = image
				tag = 'latest'	# Default tag

			# Pull the Docker image
			try:
				print(f"\nPulling : {image_name}:{tag}\n")
				subprocess.run(['docker', 'pull', f'{image_name}:{tag}'], check=True)
			except subprocess.CalledProcessError as e:
				print(f"Failed to pull image {image_name}:{tag}. Error: {e}")
				continue

			# Write the docker tag and push commands to the output file
			file.write(f"docker tag {image_name}:{tag} {local_registry}/{image_name}:{tag}\n")
			file.write(f"docker push {local_registry}/{image_name}:{tag}\n\n")

# PLEASE DEFINE AS REQUIRED
local_registry = 'localhost:5000'  # Replace with your local registry address

repo_name = 'https://github.com/harness/helm-charts.git'
input_file = 'helm-charts/src/harness/images.txt'  # File containing Docker image names
output_file = 'push2Registry.sh'


# Create the parser
parser = argparse.ArgumentParser(description="Process arguments.")

# Add the --skip-clone argument
parser.add_argument('--skip-clone', action='store_true', help='Skip cloning the git repo')

# Parse the arguments
args = parser.parse_args()

# Check if --skip-clone is set
if args.skip_clone:
    print("Skipping clone process as per the argument.")
else:
	clone_repo(repo_name)

process_docker_images(input_file, output_file, local_registry)

print(f"\n\nSummary:")
print(f"\n\t* Created script : {output_file}")
print(f"\t* Please login/authenticate against registry : {local_registry}.")
print(f"\t* Once logged in, please execute the script to push images to the registry.\n\n")

