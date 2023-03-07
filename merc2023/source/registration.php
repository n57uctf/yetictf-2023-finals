<?php include('server.php') ?>
<?php 
  if (!$_SESSION['valid']) : header('Location: ../index.php');
  elseif (isset($_SESSION['token'])) : header('location: ../cabinet.php');
  else :
?>
<?php include('header.php') ?>
<div style="text-align: center;">
Welcome to Merchant Endeavours Regarding Commandos! </br>Please, fill out registration form down below to proceed with your business here:</br></br>
</div>
  <form enctype="multipart/form-data" method="post" action="registration.php">
  	<fieldset class="tui-fieldset tui-border-solid full-width">
	<table class="tui-table-grid"><tbody>
  	  <tr><td>First Name</td>
  	  <td><input class="tui-input orange-168" type="text" name="first_name"></td></tr>
  	  <tr><td>Last Name</td>
  	  <td><input class="tui-input orange-168" type="text" name="last_name"></td></tr>
  	  <tr><td>Date of Birth</td>
  	  <td><input class="tui-input orange-168" type="date" name="dob"></td></tr>
  	  <tr><td><button type="submit" class="tui-button" name="registration" style="width:150px">Submit</button></td></tr>
	</tbody></table>
	</fieldset>
  </form>
    <div style="margin-top:100px">
  <?php include('errors.php'); ?>
</div>
<?php include('footer.php') ?>
<?php endif;?>