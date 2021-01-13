% rebase('inside-base.tpl', title='File Upload', username=username, name=name, is_admin=is_admin)
<h1>Encryption key upload</h1>
<p>Please upload encryption keys here.</p>
<p class="alert alert-danger">IMPORTANT! Keep the file name EXACTLY as the computer name!</p>
<form action="/upload" method="post" enctype="multipart/form-data">
  <label for="file" class="form-label">Key file:</label>
  <div class="input-group mb-3">
    <span class="input-group-text"><i class="bi-key"></i></span>
    <input type="file" class="form-control" name="upload" />
  </div>
  <button class="btn btn-primary" type="submit">Upload <i class="bi-upload"></i></button>
</form>
