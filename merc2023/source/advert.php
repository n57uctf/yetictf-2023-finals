<?php 
  include('server.php');
  if (!isset($_SESSION['token'])) : header('Location: ../index.php');
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
  <div class="tui-window orange-168 centered">
        <fieldset class="tui-fieldset" style="height:400px; width:600px; font-size:24px;">
        <?php if (file_exists('applications/'. $_SESSION['first_name'] . $_SESSION['last_name'] .'')):?>
            <br><br>Thank you!<br><br>
            Now you will need to wait until we're done processing your application.
            <br><form method="get" enctype="multipart/form-data" style="display: inline">
            <br><br><button type="submit" formaction="applications/<?php echo $_SESSION['first_name'] . $_SESSION['last_name'];?>" class="tui-button" style="width: 200px">Get archive</button>
            </form><form method="get" enctype="multipart/form-data" style="display: inline">
            <button type="submit" formaction="cabinet.php" class="tui-button red-168" style="width: 200px">Go back</button>
            </form>
        <?php else:?>
            <br><br>Become a merc yourself!<br><br>
            Send us an archive with personal achievements and we will find a good application for your set of skills particularly.
            <br><br>
            <form method="post" enctype="multipart/form-data" action="advert.php" style="display: inline">
            <input type="file" class="tui-input full-width white-168" name="CV"><br><br>
            <button type="submit" formaction="advert.php" name="application" class="tui-button" style="width: 200px">Apply</button></form>
            <form method="get" enctype="multipart/form-data" style="display: inline">
            <button type="submit" formaction="cabinet.php" class="tui-button red-168" style="width: 200px">Go back</button>
            </form>
        <?php endif;?>
        </fieldset>
  </div>
  </div>
  <?php include('errors.php');?>
<?php endif;?>