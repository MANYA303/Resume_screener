from flask import Flask, render_template, request
import os
from screener import screen_resumes

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure uploads folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        job_description = request.form.get('job_description', '').strip()
        resumes = request.files.getlist('resumes')

        # Validate inputs
        if not job_description or not resumes or resumes[0].filename == '':
            return render_template('index.html', error="Please enter a job description and upload at least one resume.")

        # Save resumes
        saved_files = []
        for resume in resumes:
            filename = resume.filename
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            resume.save(path)
            saved_files.append(path)

        # Process resumes
        results = screen_resumes(job_description, saved_files)
        return render_template('results.html', results=results)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)



