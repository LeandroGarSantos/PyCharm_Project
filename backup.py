from flask import Flask, render_template, request, redirect, url_for
import json
import os


app = Flask(__name__)

json_file = 'blog_posts.json'


# check if has a file JSON already
if os.path.exists(json_file):
    with open(json_file, 'r') as file:
        blog_posts = json.load(file)
else:
    # Define the data structure for blog posts
    blog_posts = [
        {'id': 1, 'author': 'John Doe', 'title': 'First Post', 'content': 'This is my first post.'},
        {'id': 2, 'author': 'Jane Doe', 'title': 'Second Post', 'content': 'This is another post.'},
        # More blog posts can go here...
    ]
    # Save the initial blog posts to the JSON file
    with open(json_file, 'w') as file:
        json.dump(blog_posts, file)


# # Save the data structure to a JSON file
# def save_posts():
#     with open(json_file, 'w') as file:
#         json.dump(blog_posts, file)


@app.route('/')
def home():
    if not blog_posts:
        return "No blog posts found."
    # Pass the blog posts to the template for rendering
    return render_template('index.html', blog_posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        post_id = int(request.form['id'])
        author = request.form['author']
        title = request.form['title']
        content = request.form['content']

        # Check if the provided ID already exists
        if any(post['id'] == post_id for post in blog_posts):
            return "ID already exists. Please choose a different ID."

        # Create a new blog post dictionary
        new_post = {'id': post_id, 'author': author, 'title': title, 'content': content}

        # Add the new blog post to the list
        blog_posts.append(new_post)

        # Save the updated blog posts to the JSON file
        with open('blog_posts.json', 'w') as file:
            json.dump(blog_posts, file)

        return redirect(url_for('home'))

    # If it's a GET request or any other request, display the add.html template
    return render_template('add.html')


@app.route('/delete/<int:post_id>', methods=['GET', 'POST'])
def delete(post_id):
    # Find the blog post with the given id and remove it from the list
    for post in blog_posts:
        if post['id'] == post_id:
            blog_posts.remove(post)
            break

    # Save the updated blog posts to the JSON file
    with open('blog_posts.json', 'w') as file:
        json.dump(blog_posts, file)

    # Redirect back to the home page
    return redirect(url_for('home'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    # Find the blog post with the given id
    for post in blog_posts:
        if post['id'] == post_id:
            if request.method == 'POST':
                # Update the blog post with the submitted data
                post['author'] = request.form['author']
                post['title'] = request.form['title']
                post['content'] = request.form['content']

                # Save the updated blog posts to the JSON file
                with open('blog_posts.json', 'w') as file:
                    json.dump(blog_posts, file)

            # If it's a GET request or any other request, display the update.html template
            return render_template('update.html', post=post)

    # If no blog post is found with the given id, redirect back to the home page
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run()