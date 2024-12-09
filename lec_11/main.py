import requests

BASE_URL = "https://jsonplaceholder.typicode.com"

def fetch_posts():
    try:
        response = requests.get(f"{BASE_URL}/posts")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching posts: {e}")
        return []

def filter_titles(posts):
    return [post for post in posts if len(post['title'].split()) <= 6]

def filter_bodies(posts):
    return [post for post in posts if post['body'].count("\n") <= 2]

def create_post():
    new_post = {
        "title": "Fresh New Post",
        "body": "This is the body of the new post. Excited to share!",
        "userId": 1
    }
    try:
        response = requests.post(f"{BASE_URL}/posts", json=new_post)
        response.raise_for_status()
        print("Post created successfully:", response.json())
    except requests.RequestException as e:
        print(f"Error creating post: {e}")

def update_post(post_id):
    updated_post = {
        "title": "Updated Post Title",
        "body": "This post has been updated successfully.",
        "userId": 1
    }
    try:
        response = requests.put(f"{BASE_URL}/posts/{post_id}", json=updated_post)
        response.raise_for_status()
        print("Post updated successfully:", response.json())
    except requests.RequestException as e:
        print(f"Error updating post: {e}")

def delete_post(post_id):
    try:
        response = requests.delete(f"{BASE_URL}/posts/{post_id}")
        if response.status_code == 200:
            print(f"Post {post_id} deleted successfully.")
        else:
            print(f"Failed to delete post {post_id}.")
    except requests.RequestException as e:
        print(f"Error deleting post: {e}")

if __name__ == "__main__":
    print("Fetching Posts...")
    posts = fetch_posts()

    print("\nFiltered Titles (6 or fewer words):")
    for post in filter_titles(posts):
        print(f"- {post['title']}")

    print("\nFiltered Bodies (3 or fewer lines):")
    for post in filter_bodies(posts):
        print(f"- {post['body']}")

    print("\nCreating a New Post:")
    create_post()

    print("\nUpdating Post with ID 1:")
    update_post(1)

    print("\nDeleting Post with ID 1:")
    delete_post(1)
