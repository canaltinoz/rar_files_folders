def upload_and_compress_folder(request):
    if request.method == 'POST':
        uploaded_files = request.FILES.getlist('posts')
        temp_dir = tempfile.mkdtemp()
        try:
            # Check if an existing zip file exists
            existing_zip = os.path.join(temp_dir, 'compressed_files.zip')

            if os.path.exists(existing_zip):
                with zipfile.ZipFile(existing_zip, 'a', zipfile.ZIP_DEFLATED) as zipf:
                    for uploaded_file in uploaded_files:
                        arcname = uploaded_file.name
                        file_path = os.path.join(temp_dir, arcname)
                        with open(file_path, 'wb') as destination:
                            for chunk in uploaded_file.chunks():
                                destination.write(chunk)
                        zipf.write(file_path, arcname)
            else:
                with zipfile.ZipFile(existing_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for uploaded_file in uploaded_files:
                        arcname = uploaded_file.name
                        file_path = os.path.join(temp_dir, arcname)
                        with open(file_path, 'wb') as destination:
                            for chunk in uploaded_file.chunks():
                                destination.write(chunk)
                        zipf.write(file_path, arcname)

            with open(existing_zip, 'rb') as zip_file:
                response = HttpResponse(zip_file.read(), content_type='application/zip')
                response['Content-Disposition'] = f'attachment; filename=compressed_files.zip'
                return response
        finally:
            shutil.rmtree(temp_dir)

    return render(request, 'upload_and_compress_folder.html')