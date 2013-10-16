#!/usr/bin/env php
<?php
require_once __DIR__.'/common.inc.php';

$lQuest = require ROOT.'config/allQuests.php';

echo 'digraph royalstory {', "\n";
echo 'node [shape = "record", fontsize = 9];', "\n";
echo 'rankdir = LR', "\n";
echo 'peripheries = 2', "\n";

foreach ($lQuest as $aQuest) {
	$aQuest += array(
		'next' => array(),
	);

	$sColor = '';
	$sAttr = '';
	switch ((string)$aQuest['npc']['primary']) {
		case 'Gnome':
			$sColor = '#D0A9F5';
			break;
		case 'PattyNPC':
			$sColor = '#F3F781';
			break;
		case 'SmallTurtle':
			$sColor = '#9AFE2E';
			break;
		case 'BertMama':
			$sColor = '#F5A9A9';
			break;
		case 'Bert':
			$sColor = '#FFBF00';
			break;
		case 'Solomon':
			$sColor = '#2EFEF7';
			break;
		case 'MightyMerella':
			$sColor = '#F781D8';
			break;
		default:
			$sColor = '';
			break;
	}

	if ($sColor) {
		$sAttr = ' [style = filled, fillcolor = "'.$sColor.'"]';
	}
	echo '"'.$aQuest['ident'].'"'.$sAttr.';', "\n";

	foreach ($aQuest['next'] as $sNext) {
		echo '"'.$aQuest['ident'].'" -> "'.$sNext.'";', "\n";
	}
}

echo "}\n";

