<!DOCTYPE html>
<html>
  <head>
    <title>Enable admin</title>
    <meta charset="utf-8" />
  <script src="https://code.jquery.com/jquery-3.5.1.min.js" integrity="sha256-9/aliU8dGd2tb6OSsuzixeV4y/faTqgFtohetphbbj0=" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
    <link rel="stylesheet" href="/static/custom.css">
    <script>
      $(document).ready(function() {
        // Clear data of previous logins
        window.localStorage.clear();
        // Clear local storage
        $('#login').submit(function() {
          if (!$('#password-input').val()) {
            alert('Please insert a password.');
            return false;
          }
        });
      });
    </script>
  </head>
  <body>
    <div class="container">
      <h1>Admin login <br><small> Enable admin mode with caution!</small></h1>
      <p>To become an admin, please enter the password below.</p>
      <form id="enable_admin" action="/enable_admin" method="post">
        
        <div class="form-group">
          <label for="password">Admin's super secret password: </label>
          <input type="password" class="form-control" id="password-input" name="password" />
        </div>
        <button type="submit" class="btn btn-default">Submit</button> 
      </form>
    </div>
  </body>
</html>
