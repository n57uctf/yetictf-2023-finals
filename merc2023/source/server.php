<?php
session_start();

$errors = array(); 

$_SESSION['db_string'] = @"host=postgres port=5432 dbname=merc user=user password=".getenv('DB_PASSWORD');

$db_connect = @pg_connect($_SESSION['db_string']);

function get_token($first_name, $last_name, $dob){
  $auth = exec("./media/encoder ".$first_name . $last_name . $dob."");
  return $auth;
}

function set_session_info($profile_info){
  $_SESSION['first_name'] = $profile_info['first_name'];
  $_SESSION['last_name'] = $profile_info['last_name'];
  $_SESSION['dob'] = $profile_info['dob'];
  $_SESSION['description'] = $profile_info['description'];
}

function encoder($token){
  $auth = exec("./media/encoder ".$token."");
  return $auth;
}

$UA_parts = explode(":",$_SERVER['HTTP_USER_AGENT']);
if (array_key_exists('HTTP_USER_AGENT', $_SERVER)){
if (!isset($_SESSION['valid'])){
if ($UA_parts[0] == 'MERCOS v3.0'){
  $_SESSION['valid'] = TRUE;
} else {
  $_SESSION['valid'] = FALSE;
}
} elseif (!isset($_SESSION['token'])&& count($UA_parts) >= 2) {
  $token = explode(":",$_SERVER['HTTP_USER_AGENT'])[1];

  if (empty($token)) {
  	array_push($errors, "Token is required");
  } elseif (preg_match("/[<,>,\",',{,},$,|,:,*,?,\\,\/]/", $token)) {
    array_push($errors, "Forbidden symbols found!");
  } elseif (encoder($token) == 'AxG64R72H65L76L66H69R82') {
    $_SESSION['status'] = '1';
    $_SESSION['token'] = 'AxG64R72H65L76L66H69R82';
    array_push($errors, '**');
  }

  if (count($errors) == 0) {
  	$query = "SELECT * FROM tokens WHERE token='$token'";
  	$results = pg_query($db_connect, $query);
    $token_check = pg_fetch_assoc($results);
  	if (pg_num_rows($results)) {
  	  $_SESSION['status'] = $token_check['status'];
      $_SESSION['token'] = $token_check['token'];
      $results = pg_query($db_connect, "SELECT * FROM profiles WHERE token='$token'");
      $profile_info = pg_fetch_assoc($results);
      set_session_info($profile_info);
  	  header('location: cabinet.php');
      exit();
  	}
  }
}
} else { $_SESSION['valid'] = FALSE; }

if (isset($_POST['registration'])) {
  $first_name = pg_escape_string($db_connect, $_POST['first_name']);
  $last_name = pg_escape_string($db_connect, $_POST['last_name']);
  $dob = pg_escape_string($db_connect, $_POST['dob']);

  if (empty($first_name)) { array_push($errors, "First name is required"); } else { 
      if (preg_match("/[<,>,\",',{,},$,|,:,*,?,\\,\/]/", $first_name)) {array_push($errors, "Forbidden symbols found!");}
  }
  if (empty($last_name)) { array_push($errors, "Last name is required"); } else { 
    if (preg_match("/[<,>,\",',{,},$,|,:,*,?,\\,\/]/", $last_name)) {array_push($errors, "Forbidden symbols found!");}
  }
  if (empty($dob)) { array_push($errors, "Date of Birth is required"); }

  $token = get_token($first_name, $last_name, $dob);

  if (isset($_POST['description'])){
    $description = pg_escape_string($db_connect, $_POST['description']);
    $descripion = substr($description,0,64);
    $status = "Merc";
    if (isset($_FILES['avatar']) && $_FILES['avatar']['size'] < 10000 && $_FILES['avatar']['type'] == 'image/jpeg'){
      move_uploaded_file($_FILES['avatar']['tmp_name'],'avatars/'.$descripion.'');
    }
  } else {
    $description = "";
    $status = "Merchant";
  }

  if (count($errors) == 0) {
    $user_check_query = "SELECT * FROM tokens WHERE token='$token' LIMIT 1";
    $result = pg_query($db_connect, $user_check_query);
    $token_check = pg_fetch_assoc($result);
  
    if ($token_check) { 
      array_push($errors, "User with those parameters already exists");
    }
  }

  if (count($errors) == 0) {
  	@pg_query($db_connect, "INSERT INTO tokens (token, status)
          VALUES('$token', '$status')");
    @pg_query($db_connect, "INSERT INTO profiles (token, first_name, last_name, dob, description)
        VALUES('$token', '$first_name', '$last_name', '$dob', '$description')");
  	$_SESSION['token'] = $token;
    $_SESSION['status'] = $status;
    $results = pg_query($db_connect, "SELECT * FROM profiles WHERE token='$token'");
    if (pg_num_rows($results) != 0) {
      $profile_info = pg_fetch_assoc($results);
      set_session_info($profile_info);
  	  header('location: cabinet.php');
      exit();
    } else {
      array_push($errors, "Something went wrong");
    }
  }
}

if (isset($_POST['request']) && isset($_SESSION['token'])) {
  $alias = pg_escape_string($db_connect, $_POST['alias']);
  $payment = pg_escape_string($db_connect, $_POST['payment']);
  $location = pg_escape_string($db_connect, $_POST['location']);
  $commentary = pg_escape_string($db_connect, $_POST['commentary']);
  $theme = pg_escape_string($db_connect, $_POST['theme']);
  $contractor_token = $_SESSION['token'];
  $contractor_alias = $_SESSION['first_name'];

  if (empty($alias)) {
    array_push($errors, "Commando's alias is needed!");
  }
  if (empty($payment) || $payment < 0 || !is_numeric($payment)) {
    array_push($errors, "Write how much you offer!");
  }
  if ($payment > 100000) {
    array_push($errors, "You don't have those numbers, kid");
  }
  if (empty($location)) {
    array_push($errors, "Location needed!");
  }
  if (empty($commentary)) {
    $commentary = "None";
  }
  if (empty($theme)) {
    $theme = "Hiring ".$alias."";
  }
  if (preg_match("/[<,>,\",',{,},$,|,:,*,?,\\,\/]/", $commentary)) 
  {
    array_push($errors, "Forbidden symbols found!");
  }

  if (count($errors) == 0) {
    $timemark = date('h:i');
    $commentary = substr($commentary,0,64);
    $theme = substr($theme,0,64);
    $results = pg_query($db_connect, "SELECT token FROM profiles WHERE description='$alias' ORDER BY id DESC LIMIT 1");
    if (pg_num_rows($results) == 1) {
      $executor_token = pg_fetch_assoc($results)['token'];
      @pg_query($db_connect, "INSERT INTO contracts (contractor_token, executor_token, location, payment, commentary) VALUES('$contractor_token', '$executor_token', '$location', '$payment', '$commentary')");
      @pg_query($db_connect, "INSERT INTO messages (sender_id, receiver_id, theme, message, timemark) VALUES('$contractor_token', '$executor_token', '$theme', '$commentary', '$timemark')");
      header('location: cabinet.php');
      exit();
    } else {
      array_push($errors,'No commando goes by that alias');
    }
  }
}

if (isset($_POST['message']) && isset($_SESSION['token'])) {
  $theme = pg_escape_string($db_connect, $_POST['theme']);
  $contents = pg_escape_string($db_connect, $_POST['contents']);
  $receiver = pg_escape_string($db_connect, $_POST['receiver']);
  $timemark = date('h:i');

  $sender_id = $_SESSION['token'];
  if (empty($receiver) || empty($theme) || empty($contents) || !isset($_SESSION['token'])) {
    array_push($errors, "Failed to send message, refill form.");
  }

  $receiver_data = explode(":",$receiver);
  $first_name = $receiver_data[0];
  $last_name = $receiver_data[1];
  $results = pg_query(pg_connect($_SESSION['db_string']),"SELECT token FROM profiles WHERE (first_name='$first_name' AND last_name='$last_name')");
	if (pg_num_rows($results) != 0) $receiver_id = pg_fetch_all($results)[0]['token'];

  if (!isset($receiver_id)) array_push($errors, "No such profile found");

  if (count($errors) == 0) {
    @pg_query($db_connect, "INSERT INTO messages (sender_id, receiver_id, theme, message, timemark) 
          VALUES('$sender_id', '$receiver_id','$theme', '$contents', '$timemark')");
    header('location: messenger.php');
  }
}

if (isset($_POST['application']) && isset($_SESSION['token'])) {
  if (isset($_FILES['CV']) && $_FILES['CV']['size'] < 10000 && $_FILES['CV']['type'] == 'application/zip'){
    move_uploaded_file($_FILES['CV']['tmp_name'],'applications/'. $_SESSION['first_name'] . $_SESSION['last_name'] .'');
  } else {
    array_push($errors, "Attach a valid archive");
  }
}

if (isset($_POST['security']) && isset($_SESSION['token'])) {
  $token = $_SESSION['token'];
  
  if (empty($token)) {
    array_push($errors, "No Token provided!");
  }

  if (count($errors) == 0) {
    $results = pg_query($db_connect, "SELECT * FROM profiles WHERE token='$token' LIMIT 1");
    if (pg_num_rows($results) == 1) {
    $profile_info = pg_fetch_assoc($results);
    $new_token = get_token($profile_info['first_name'], $profile_info['last_name'], $profile_info['dob']);
    $first_name = $profile_info['first_name'];
    $last_name = $profile_info['last_name'];
    $dob = $profile_info['dob'];
    $description = $profile_info['description'];
    $status = pg_fetch_assoc(pg_query($db_connect, "SELECT * FROM tokens WHERE token='$token' LIMIT 1"))['status'];
    @pg_query($db_connect, "DELETE FROM tokens WHERE token='$token'");
    @pg_query($db_connect, "INSERT INTO tokens (token, status) VALUES('$new_token','$status')");
    @pg_query($db_connect, "DELETE FROM profiles WHERE token='$token'");
    @pg_query($db_connect, "INSERT INTO profiles (token, first_name, last_name, dob, description) VALUES('$new_token', '$first_name', '$last_name', '$dob', '$description')");
    $_SESSION['token'] = $new_token;
    header('location: cabinet.php');
    exit();
    } else {
      array_push($errors, "No profile for such Token!");
    }
  }
}

if (isset($_GET['id'])){
  $id = pg_escape_string($db_connect, $_GET['id']);
  $results = pg_query($db_connect, "SELECT * FROM profiles WHERE id='$id'");
  if (pg_num_rows($results) != 0) {
    $profile_info = pg_fetch_assoc($results);
    set_session_info($profile_info);
  }
}

if (isset($_GET['status']) && isset($_GET['cid']) && isset($_SESSION['token'])){
  $cid = pg_escape_string($db_connect, $_GET['cid']);
  $status = pg_escape_string($db_connect, $_GET['status']);
  $results = pg_query($db_connect, "SELECT * FROM contracts WHERE id='$cid' LIMIT 1");
  if (pg_num_rows($results) == 1) { 
    $contract_info = pg_fetch_assoc($results);
    $contractor_token = $contract_info['contractor_token'];
    $executor_token = $contract_info['executor_token'];
    $location = $contract_info['location'];
    $payment = $contract_info['payment'];
    $commentary = $contract_info['commentary'];
    @pg_query($db_connect, "DELETE FROM contracts WHERE id='$cid'");
    @pg_query($db_connect, "INSERT INTO contracts (contractor_token, executor_token, location,  payment, commentary, status) VALUES('$contractor_token', '$executor_token', '$location',   '$payment', '$commentary', '$status')");
  }
}

if (isset($_POST['profile']) && isset($_SESSION['token'])) {
  $token = $_SESSION['token'];
  $first_name = pg_escape_string($db_connect, $_POST['first_name']);
  $last_name = pg_escape_string($db_connect, $_POST['last_name']);
  $dob = pg_escape_string($db_connect, $_POST['dob']);
  $descripion = pg_escape_string($db_connect, $_POST['description']);

  if (empty($first_name)) { array_push($errors, "First name is required"); } else { 
      if (preg_match("/[<,>,\",',{,},$,|,:,*,?,\\,\/]/", $first_name)) {array_push($errors, "Forbidden symbols found!");}
  }
  if (empty($last_name)) { array_push($errors, "Last name is required"); } else { 
    if (preg_match("/[<,>,\",',{,},$,|,:,*,?,\\,\/]/", $last_name)) {array_push($errors, "Forbidden symbols found!");}
  }
  if (empty($dob)) { array_push($errors, "Date of Birth is required"); }

  if (empty($token)) {
    array_push($errors, "No token provided!");
  }

  if (isset($_FILES['avatar']) && $_FILES['avatar']['size'] < 10000 && $_FILES['avatar']['type'] == 'image/jpeg'){
    move_uploaded_file($_FILES['avatar']['tmp_name'],'avatars/'.$descripion.'');
  }

  if (count($errors) == 0) {
    $results = pg_query($db_connect, "SELECT * FROM profiles WHERE token='$token' LIMIT 1");
    if (pg_num_rows($results) == 1) {
    @pg_query($db_connect, "DELETE FROM profiles WHERE token='$token'");
    @pg_query($db_connect, "INSERT INTO profiles (token, first_name, last_name, dob, description) VALUES('$token', '$first_name', '$last_name', '$dob', '$description')");
    $results = pg_query($db_connect, "SELECT * FROM profiles WHERE token='$token'");
    $profile_info = pg_fetch_assoc($results);
    set_session_info($profile_info);
    header('location: cabinet.php');
    exit();
    } else {
      array_push($errors, "No profile for this token!");
    }
  }
}

if (isset($_GET['logout'])) {
    session_destroy();
    header("location: ../index.php");
    exit();
}