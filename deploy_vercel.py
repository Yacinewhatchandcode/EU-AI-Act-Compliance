"""
Auto-deploy to Vercel staging.
OpenClaw calls this after code is ready.
Usage: python deploy_vercel.py <project_dir>
"""
import subprocess
import sys
import os

def deploy(project_dir):
    """Deploy a project to Vercel staging."""
    if not os.path.isdir(project_dir):
        print(f"Error: {project_dir} is not a directory")
        sys.exit(1)

    print(f"Deploying {project_dir} to Vercel...")

    # Install dependencies
    print("Installing dependencies...")
    subprocess.run(["npm", "install"], cwd=project_dir, shell=True, check=True)

    # Build
    print("Building project...")
    subprocess.run(["npm", "run", "build"], cwd=project_dir, shell=True, check=True)

    # Deploy to Vercel (staging = preview)
    print("Deploying to Vercel staging...")
    result = subprocess.run(
        ["npx", "-y", "vercel", "--yes"],
        cwd=project_dir, shell=True,
        capture_output=True, text=True
    )

    if result.returncode == 0:
        url = result.stdout.strip().split("\n")[-1]
        print(f"SUCCESS! Staging URL: {url}")
        return url
    else:
        print(f"Deploy failed: {result.stderr}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python deploy_vercel.py <project_directory>")
        sys.exit(1)
    deploy(sys.argv[1])
