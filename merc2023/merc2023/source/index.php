<?php include('server.php') ?>
<?php 
  if ($_SESSION['valid']) : header('Location: ../registration.php');
  else :
?>
<!DOCTYPE html>
<html class="tui-bg-blue-white">
<head>
  <title>MERC</title>
  <link rel="stylesheet" href="dist/tuicss.min.css" />
  <script src="dist/tuicss.min.js"></script>
</head>
<style> 
    body { 
      font-family: 'Perfect DOS VGA\ 437 Win'; 
    } 
</style> 
<body>
<div class="tui-screen-1024-768 bordered white-168 tui-bg-orange-white centered">
<div class="center" style="margin-top: 100px; margin-bottom: 100px">
  <div class="tui-window red-168 centered">
        <fieldset class="tui-fieldset" style="height:400px; width:400px; font-size:24px;">
        <br><br><br>Service unavailable<br><br><br>
        Try again later
        </fieldset>
  </div>
  </div>
<?php endif;?>