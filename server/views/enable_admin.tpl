% rebase('inside-base.tpl', title='Enable admin', username=username, name=name, is_admin=is_admin)
<h1>Admin login</h1>
<p class="alert alert-info">Enable admin mode with caution!</p>

<form id="enable_admin" action="/enable_admin" method="post">
  <label for="password" class="form-label">Enter Admin's password: </label>
  <div class="input-group mb-3">
    <span class="input-group-text"><i class="bi-key"></i></span>
    <input type="password" class="form-control" id="password-input" name="password" />
  </div>
  <button type="submit" class="btn btn-primary"><i class="bi-shield-shaded"></i> Submit</button>
</form>
<script>
  $(document).ready(function() {
    $('#enable_admin').submit(function() {
      if (!$('#password-input').val()) {
        alert('Please insert a password.');
        return false;
      }
    });
  });
</script>
