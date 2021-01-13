% rebase('inside-base.tpl', title='Enable admin', username=username, name=name, is_admin=is_admin)
<h1>Admin login <br><small> Enable admin mode with caution!</small></h1>
<p>To become an admin, please enter the password below.</p>
<form id="enable_admin" action="/enable_admin" method="post">
  <div class="form-group">
    <label for="password">Admin's super secret password: </label>
    <input type="password" class="form-control" id="password-input" name="password" />
  </div>
  <button type="submit" class="btn btn-default">Submit</button> 
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
