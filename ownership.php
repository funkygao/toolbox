#!/usr/bin/env php
<?php
/**
 * 计算某个源代码的ownership值.
 *
 * usage:
 * find www -name '*.php' -exec ownership.php {} \;
 *
 * @author gaopeng <gaopeng@corp.kaixin001.com>
 */

function calcOwnership($filename, $threshold)
{
    $authorsCmd = "svn log $filename|grep line | cut -d' ' -f3";
    $contributors = `$authorsCmd`;
    $authorCommitCount = array();
    $totalCommitCount = 0;
    foreach (split("\n", $contributors) as $author)
    {
        if (isset($authorCommitCount[$author]))
        {
            $authorCommitCount[$author]++;
        }
        else
        {
            $authorCommitCount[$author] = 1;
        }

        $totalCommitCount++;
    }

    $majorCommits = 0;
    foreach ($authorCommitCount as $author => $count)
    {
        $percent = $count * 100 / $totalCommitCount;
        if ($percent >= $threshold)
        {
            $majorCommits += $count;
        }
    }

    $s = sprintf("%7.3f %3d %3d %s\n",
        $majorCommits * 100 / $totalCommitCount,
        $majorCommits,
        $totalCommitCount,
        $filename
    );
    echo $s;

}

$majorThreshold = 15; // 15%
if (isset($argv[2]))
{
    $majorThreshold = (int)$argv[2];
}
calcOwnership($argv[1], $majorThreshold);
