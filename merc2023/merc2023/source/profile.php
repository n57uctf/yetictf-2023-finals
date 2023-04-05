<?php include('server.php') ?>
<?php 
  if (!isset($_SESSION['token'])) : header('Location: ../index.php');
  else :
?>
<?php include('header.php')?>
<legend>Profile</legend>
<?php if ($_SESSION['status'] == "Merchant"): ?>
  <?php echo $_SERVER['HTTP_USER_AGENT']?></br></br>
  <form enctype="multipart/form-data" method="post" action="profile.php">
  <fieldset class="tui-fieldset tui-border-solid full-width">
	<table class="tui-table-grid"><tbody>
	  <tr><td>First Name</td>
  	  <td><input class="tui-input orange-168" type="text" name="first_name" style="display:table-cell" value="<?echo $_SESSION['first_name']?>"></td></tr>
  	  <tr><td>Last Name</td>
  	  <td><input class="tui-input orange-168" type="text" name="last_name" style="display:table-cell" value="<?echo $_SESSION['last_name']?>"></td></tr>
  	  <tr><td>Date of Birth</td>
  	  <td><input class="tui-input orange-168" type="date" name="dob" style="display:table-cell" value="<?echo $_SESSION['dob']?>"></td></tr>
  	  <tr style="display: none"><td>Description</td>
  	  <td><input class="tui-input orange-168" type="text" name="description" style="display:table-cell;" value=""></td></tr>
  	  <tr style="display: none"><td>Avatar upload</td>
  	  <td><input class="tui-input orange-168" type="file" name="avatar" accept="image/jpeg" style="display:table-cell"></td></tr>
  	  <tr><td><button type="submit" class="tui-button" name="profile" style="width:150px" >Submit</button></td></tr>
	  </tbody></table>
	</fieldset>
  </form>
<?php elseif ($_SESSION['status'] == "Merc"):?>
	<?php echo $_SERVER['HTTP_USER_AGENT']?>
	<form enctype="multipart/form-data" method="post" action="profile.php">
	  <fieldset class="tui-fieldset tui-border-solid full-width">
		<table class="tui-table-grid"><tbody>
		  <tr><td>First Name</td>
	  	  <td><input class="tui-input orange-168" type="text" name="first_name" style="display:table-cell" value="<?echo $_SESSION['first_name']?>"></td></tr>
	  	  <tr><td>Last Name</td>
	  	  <td><input class="tui-input orange-168" type="text" name="last_name" style="display:table-cell" value="<?echo $_SESSION['last_name']?>"></td></tr>
	  	  <tr><td>Date of Birth</td>
	  	  <td><input class="tui-input orange-168" type="date" name="dob" style="display:table-cell" value="<?echo $_SESSION['dob']?>"></td></tr>
	  	  <tr><td>Description</td>
	  	  <td><input class="tui-input orange-168" type="text" name="description" style="display:table-cell;" value="<? echo $_SESSION['description']?>"></td></tr>
	  	  <tr><td>Avatar upload</td>
	  	  <td><input class="tui-input orange-168" type="file" name="avatar" accept="image/jpeg" style="display:table-cell"></td></tr>
	  	  <tr><td><button type="submit" class="tui-button" name="profile" style="width:150px" >Submit</button></td></tr>
		  </tbody></table>
		</fieldset>
	  </form>
<?php endif;?>
<?php include('errors.php'); ?>
<?php include('footer.php')?>
<?php endif;?> 