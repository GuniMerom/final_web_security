<html><head>
  <meta http-equiv="content-type" content="text/html; charset=UTF-8">
  <script src="https://code.jquery.com/jquery-3.5.1.min.js" integrity="sha256-9/aliU8dGd2tb6OSsuzixeV4y/faTqgFtohetphbbj0=" crossorigin="anonymous"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
  <link rel="stylesheet" href="/static/custom.css">
  <script type="text/javascript" src="/static/code.js"></script>
  <title>File Upload</title>
  <script type="text/javascript">var username = "{{username}}";</script>
</head>
<body>
  <p>Welcome {{username}}, Please upload encryption key computer name and computer key.
  <br>
  <p>Don't forget to keep the file name as the computer name! 	
  <br>
  <br>
  <br>
  <br>
  <br>
  <br>
  <br>
  <br>

  <form action="/upload" method="post" enctype="multipart/form-data">
    Select a file: <input type="file" name="upload" />
    <input type="submit" value="Start upload" />
  </form>

</div>
</body>
</html>

