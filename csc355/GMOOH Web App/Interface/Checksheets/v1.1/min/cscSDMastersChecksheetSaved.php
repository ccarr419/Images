
<?php

session_start();

    require("../../../../PHPClasses/logic.class.php");

 function xml2array($fname){
//      $sxi = new SimpleXmlIterator($fname, 0, true);
     $sxi = simplexml_load_string($fname, 'SimpleXMLIterator');
      return sxiToArray($sxi);
    }

    function sxiToArray($sxi){
      $a = array();
      for( $sxi->rewind(); $sxi->valid(); $sxi->next() ) {
        if(!array_key_exists($sxi->key(), $a)){
          $a[$sxi->key()] = array();
        }
        if($sxi->hasChildren()){
          $a[$sxi->key()][] = sxiToArray($sxi->current());
        }
        else{
          $a[$sxi->key()][] = strval($sxi->current());
        }
      }
      return $a;
    }


function stripInvalidXml($value) {
    $ret = "";
    $current;
    if (empty($value)) {
        return $ret;
    }
    $length = strlen($value);
    for ($i=0; $i < $length; $i++) {
        $current = ord($value{$i});
        if (($current == 0x9) || ($current == 0xA) || ($current == 0xD) || (($current >= 0x20) && ($current <= 0xD7FF)) || (($current >= 0xE000) && ($current <= 0xFFFD)) || (($current >= 0x10000) && ($current <= 0x10FFFF))) {
                $ret .= chr($current);
        }
        else {
            $ret .= "";
        }
    }
    return $ret;
}

$goodChars = array("", "&#47;", "&#39;","&#92;","&#94;","&#126;","&#34;");
$badChars   = array("&", "/", "'","\\","^","~",'"');


    $logic = new Logic();
    $sData = "";
    $results = $logic->displaySaveFromCheck($_SESSION['userID'], $_GET['AIDID']);
    foreach ($results as $row) {
//        echo stripInvalidXml($row["SaveData"]);
//        echo preg_replace('/&(?!#?[a-z0-9]+;)/', '&amp;',$row["SaveData"]);
//        echo str_replace("And","&", stripInvalidXml($row["SaveData"]));
        $sData = xml2array(preg_replace('/&(?!#?[a-z0-9]+;)/', '&amp;',$row["SaveData"]));
        
    }


    
    //print_r($sData);
    //echo "<br><br>";
    $indexOGen = 0;
    $indexOPro = 0;
//    echo $sData["Student"][0]["Program"][0]["Class"][23]["ClassGrade"][0];
    //echo $sData["Student"][0]["GenEd"][0]["Class"][2]["ClassName"][0];


?>
<!DOCTYPE html>
<html>
	<head>
	<title>MS Computer Science: SD Checksheet</title>
	<link rel = "stylesheet" type = "text/css" href = "Styles/checksheetStyleV1p1min.css"/>
	</head>
	<body>	
<!-- #MS CSC SOFTWARE DEVELOPMENT MAJOR PROGRAM TABLE# -->
		<div class = "section">
			<table>
				<tr>
					<th class = "tableHeader" colspan = "3"><u title = "Click for notes" onclick = "showDialog('#msCSCNotes', 550, true)">
						Master Program: 30 sh</u></th>
				</tr>
				<tr>
					<th colspan = "1">&emsp;1. 400-level Courses: <b>(0-12 sh)</b></th>
						<td class = "tableGrade">Gr</td>
						<td class = "tableGrade">SH</td>
				</tr>
		<!-- 400 level courses -->			
				<?php
					for($i = 0; $i < 4; $i++){

                        
                      echo  "<tr>	
								<th class = 'courseBox'><div id = 'MS CSC:SD 400-Level' onclick = 'findCourses(this)' class = 'courseNameBox courseNameBoxPro'>"."<span id='proClass" .$indexOPro."'>&#8195;".$sData["Student"][0]["Program"][0]["Class"][$indexOPro]["ClassName"][0] . "</span>" ."</div></th>
								<td  class = 'tableGrade'><input class = 'gradeBox' id = 'proGrade".$indexOPro."' type = 'text' maxlength = '2' />".$sData["Student"][0]["Program"][0]["Class"][$indexOPro]["ClassGrade"][0]."</td>
								<td  class = 'tableGrade'></td>
							</tr>";
                        
//                        
//						echo "<tr>	
//								<th class = 'courseBox'><div id = 'MS CSC:SD 400-Level' onclick = 'findCourses(this)' class = 'courseNameBox courseNameBoxPro'>"."<span id='proClass" .$indexOPro."'>".$sData["Student"][0]["Program"][0]["Class"][$indexOPro]["ClassName"][0] . "</span>" ."</div></th>
//								<td  class = 'tableGrade'><input class = 'gradeBox' id = 'proGrade".$indexOPro."' type = 'text' maxlength = '2' />".$sData["Student"][0]["Program"][0]["Class"][$indexOPro]["ClassGrade"][0]."</td>
//
//								<td  class = 'tableGrade'></td>
//							</tr>";
							$indexOPro++;
							}
				?>	
		<!-- 500 level courses -->
				<tr>	
					<th colspan = "1">&emsp;2. 500-level Courses: <b>(18-30 sh)</b></th>
					<td class = "tableGrade">Gr</td>
					<td class = "tableGrade">SH</td>
				</tr>			
				<?php
					for($i = 0; $i < 10; $i++){
						echo "<tr>	
								<td>"."<span id='proClass" .$indexOPro."'>&#8195;".$sData["Student"][0]["Program"][0]["Class"][$indexOPro]["ClassName"][0] . "</span>" ."</div></th>
								<td  class = 'tableGrade'><input class = 'gradeBox' id = 'proGrade".$indexOPro."' type = 'text' maxlength = '2' />".$sData["Student"][0]["Program"][0]["Class"][$indexOPro]["ClassGrade"][0]."</td>
								<td  class = 'tableGrade'></td>
							</tr>";
                        
							$indexOPro++;
							}
				?>	
			</table>
            <input type="hidden" id="programID" value="GLASCSC" />
            <?php 
                echo "<input type='hidden' id='programCount' value='".$indexOPro."'  />";
            ?>			
		</div>
	</body>
</html>
			
