<?php 
  include('server.php');
  if (!isset($_SESSION['token'])) : header('Location: ../index.php');
  else :
?>
<?php include('header.php') ?>
<legend>Browser</legend>
<table class="tui-table-grid no-border" style="width: 100%; height:70%">
    <thead class="white-255-text orange-168-border" style="height:20%">
        <tr>
        <th style="width: 25%"><hr class="tui-divider"></hr></th>
        <th style="width: 20%">Alias</th>
        <th style="width: 15%">Experience</th>
        <th style="width: 15%">Weekly $ fee</th>
        <th style="width: 15%"><hr class="tui-divider"></hr></th></tr>
    </thead>
    <tbody class="white-255-text tui-border-double orange-168-border">
        <tr>
        <?php 
          $results = pg_query(pg_connect($_SESSION['db_string']), "SELECT * FROM commandos");
          if (pg_num_rows($results) != 0) {
            $commandos = pg_fetch_all($results);
            if (isset($_GET['page']) && is_numeric($_GET['page']) && $_GET['page'] > 0){
                $offset = $_GET['page'] - 1;
            } else {
                $offset = 0;
            }
            for ($i = $offset*3; $i < $offset*3 + 3 && $i < count($commandos); $i++) :?><?php 
            echo '<td><a href="merc.php?alias='.$commandos[$i]['alias'].'"><img src="avatars/'.$commandos[$i]['alias'].'.jpg" style="width:80px;height:92px;image-rendering:pixelated;"></a></td><td><p style="text-align:center;">'.$commandos[$i]['alias'].'</p></td><td><p style="text-align:center;">'.$commandos[$i]['xp'].'</p></td><td><p style="text-align:center;">'.$commandos[$i]['price'].'</p></td><td><form method="get"><p style="text-align:center;">';
            if ($commandos[$i]['status']) {
                echo '<button type="submit" formaction="merc.php" name="alias" value="'.$commandos[$i]['alias'].'" class="tui-button" style="width: 200px">Hire</button></p></td></tr>';
            } else {
                echo '<button type="submit" formaction="merc.php" class="tui-button red-168 disabled" style="width: 200px" disabled>Unavailable</button></p></td></tr></form>';
            } 
            endfor;
        }?>
        </tr>
    </tbody>
</table>
<?php if(isset($offset)):?>
<form method="get">
<div class="tui-window orange-168" style="position:absolute; width: 668px; left: 18px; bottom:15px">
    <fieldset class="tui-fieldset tui-border-solid center">
<?php if ($offset > 0 && (($offset + 1)*3) >= count($commandos)):?>
    <button type="submit" formaction="browser.php" name="page" value="<?echo $offset?>" class="tui-button left" style="width: 200px">Previous</button>
    <span class="center">Page <?php echo $offset + 1?>/<?php echo ceil(count($commandos)/3)?></span>
    <button type="submit" formaction="browser.php" name="page" value="<?echo $offset+2?>" class="tui-button red-168 disabled right" style="width: 200px" disabled>Next</button>
<?php elseif ((($offset + 1)*3) <= count($commandos) && $offset != 0):?>
    <button type="submit" formaction="browser.php" name="page" value="<?echo $offset?>" class="tui-button left" style="width: 200px">Previous</button>
    <span class="center">Page <?php echo $offset + 1?>/<?php echo ceil(count($commandos)/3)?></span>
    <button type="submit" formaction="browser.php" name="page" value="<?echo $offset+2?>" class="tui-button right" style="width: 200px">Next</button>
<?php elseif (count($commandos) <= 3):?>
    <button type="submit" formaction="browser.php?" name="page" value="<?echo $offset?>" class="tui-button red-168 disabled left" style="width: 200px" disabled>Previous</button>
    <span class="center">Page <?php echo $offset + 1?>/<?php echo ceil(count($commandos)/3)?></span>
    <button type="submit" formaction="browser.php" name="page" value="<?echo $offset+2?>" class="tui-button red-168 disabled right" style="width: 200px" disabled>Next</button>
<?php else:?>
    <button type="submit" formaction="browser.php?" name="page" value="<?echo $offset?>" class="tui-button red-168 disabled left" style="width: 200px" disabled>Previous</button>
    <span class="center">Page <?php echo $offset + 1?>/<?php echo ceil(count($commandos)/3)?></span>
    <button type="submit" formaction="browser.php" name="page" value="<?echo $offset+2?>" class="tui-button right" style="width: 200px">Next</button>
<?php endif;?>
</fieldset>
</div>
</form>
<?php endif;?>
<?php include('footer.php') ?>
<?php endif;?>