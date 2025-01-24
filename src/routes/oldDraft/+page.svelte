<script>

  //import { Table, TableBody, TableBodyCell, TableBodyRow, TableHead, TableHeadCell } from 'flowbite-svelte';

    
    const { data } = $props();
    //console.log(data)


    //////////////////////////////////////
    // first scatterplot
    //////////////////////////////////////

    let scatter_right_shear = 40
    let scatter_bottom_shear = 40

    let scatter_height = 360 + 60
    let scatter_width = 360 + 100


    let scatter_x_max = 230
    let scatter_x_num = scatter_x_max / 20
    let scatter_x_ticks = [scatter_x_num]
    for (let i = 0; i < scatter_x_num; i++){
        scatter_x_ticks[i] = 20 * i
    }

    let scatter_y_ticks = scatter_x_ticks


    /**
	 * @param {any} a
	 */
    function scatter_scale_x (a) { return a * 1.5 + scatter_right_shear}

    /**
	 * @param {any} a
	 */
    function scatter_scale_y (a) { return scatter_height - (a * 1.5) - scatter_bottom_shear}

    ////////////////////////////////////////////////
    // end of first scatterplot
    ////////////////////////////////////////////////



    ////////////////////////////////////////////////
    // first line chart
    ////////////////////////////////////////////////

    let line_right_shear = 65
    let line_bottom_shear = 70

    let line_height = 320 + 100
    let line_width = 360 + 100

    /**
	 * @param {any} a
	 */
    function line_calc_group (a) {
        let temp = Math.floor((a-1896)/20)
        if (temp <= 0){
            temp = 1
        }
        else if (temp >= 7){
            temp = 6
        }
        return temp
    }
    
    /**
     * @param {any} a
     */
        function line_calc_group_x (a) {
            return a * 50 + line_right_shear
        }

    /**
	 * @param {any} a
	 */
    function line_scale_y (a) { 
        return line_height - (a /70) - line_bottom_shear
    }

    let medals = [0,0,0,0,0,0]
    let groups = [1,2,3,4,5,6]
    data.olymCSV.forEach((/** @type {{ Year: any; }} */ element) => {
        let group = line_calc_group(element.Year)
        medals[group-1] = medals[group-1] + 1
    });
    console.log("Medals: " + medals)

    let line_x_ticks1 = ["1896", "1918", "1938", "1958", "1978", "1998"]
    let line_x_ticks2 = ["1916", "1936", "1956", "1976", "1996", "2016"]
    let line_y_ticks = []
    for (let i = 1; i < 11; i++){
        line_y_ticks[i-1] = 2000 * i
    }

    ////////////////////////////////////////////////
    // end of line chart
    ////////////////////////////////////////////////


    ////////////////////////////////////////////////
    // begin pie chart
    ////////////////////////////////////////////////
    let summer = 0
    let winter = 0
    
    data.olymCSV.forEach((/** @type {{ Season: any; }} */ element) => {
        let seas = element.Season
        if (seas == "Summer"){
            summer++
        }
        else {
            winter++
        }
    });

    let total = summer + winter
    let deg_border = (winter / total) * 360

    /////////////////////////////////////////////////
    // end pie
    /////////////////////////////////////////////////

</script>

<div style="margin-bottom: 10px;">
    <text style="font-size: 30px;font-style: bold;">Olympic Data</text>
    <text style="margin-left: 20px;">Source: <a href="https://www.kaggle.com/datasets/bhanupratapbiswas/olympic-data">Kaggle</a></text>
    <text style="margin-left: 20px;"><a href="../">New Page</a></text>
</div>


<div style="float: left;">
<div class="box" style="margin-right: 10px;">
<!-- scatter plot -->
<svg width="{scatter_width}" height="{scatter_height}">
    {#each data.olymCSV as datapoint}
        <circle cx="{scatter_scale_x(datapoint.Weight)}" cy="{scatter_scale_y(datapoint.Height)}" r="3" />
    {/each}
    
    <line class="axis" id="x" x1="{scatter_scale_x(0)-5}" y1="{scatter_scale_y(0)}" x2="{scatter_scale_x(scatter_x_max+5)}" y2="{scatter_scale_y(0)}" />
    <line class="axis" id="y" x1="{scatter_scale_x(0)}" y1="{scatter_scale_y(0)-5}" x2="{scatter_scale_x(0)}" y2="{scatter_scale_y(scatter_x_max+5)}" />

    <text x="{scatter_scale_x(scatter_x_max+10)}" y="{scatter_scale_y(0)+5}">Weight</text>
    <text x="{scatter_scale_x(scatter_x_max+10)}" y="{scatter_scale_y(0)+25}">(kg)</text>
    <text x="{scatter_scale_x(0)-35}" y="{scatter_scale_y(scatter_x_max+10)}">Height (cm)</text>

    {#each scatter_x_ticks as tick}
        <line class="tick" x1="{scatter_scale_x(tick)}" y1="{scatter_scale_y(0)+5}" x2="{scatter_scale_x(tick)}" y2="{scatter_scale_y(0)-5}" />
        <text class="ticks" id="x_ticks" x="{scatter_scale_x(tick)}" y="{scatter_scale_y(0)+5}">{tick}</text>
    {/each}

    {#each scatter_y_ticks as tick}
        <line class="tick" x1="{ scatter_scale_x(0)-5}" y1="{scatter_scale_y(tick)}" x2="{ scatter_scale_x(0)+5}" y2="{scatter_scale_y(tick)}" />
        <text class="ticks" x="{scatter_scale_x(0)-35}" y="{scatter_scale_y(tick)+7}">{tick}</text>
    {/each}
</svg>
</div>

<!-- line plot -->
<div class="box" style="margin-right: 10px;">
<svg width="{line_width}" height="{line_height}">
    {#each groups as i}
        <line class="bar" x1="{line_calc_group_x(i)}" y1="{line_scale_y(0)}" x2="{line_calc_group_x(i)}" y2="{line_scale_y(medals[i-1])}" />
    {/each}
    
    <line class="axis" id="x" x1="{line_calc_group_x(0)-5}" y1="{line_scale_y(0)}" x2="{line_calc_group_x(6)+20}" y2="{line_scale_y(0)}" />
    <line class="axis" id="y" x1="{line_calc_group_x(0)}" y1="{line_scale_y(0)+5}" x2="{line_calc_group_x(0)}" y2="{line_scale_y(22500)}" />

    <text x="{line_calc_group_x(6)+20}" y="{line_scale_y(0)+5}">Year</text>
    <text x="{line_calc_group_x(0)-37}" y="{line_scale_y(22500)-10}">Medals</text>
    
    {#each groups as tick}
        <line class="tick" x1="{line_calc_group_x(tick)}" y1="{line_scale_y(0)+5}" x2="{line_calc_group_x(tick)}" y2="{line_scale_y(0)-5}" />
        <text class="ticks" id="x_ticks" x="{line_calc_group_x(tick)+9}" y="{line_scale_y(0)+5}">{line_x_ticks1[tick-1]+" -"}</text>
        <text class="ticks" id="x_ticks" x="{line_calc_group_x(tick)-9}" y="{line_scale_y(0)+5}">{line_x_ticks2[tick-1]}</text>
    {/each}

    
    {#each line_y_ticks as tick}
        <line class="tick" x1="{ line_calc_group_x(0)-5}" y1="{line_scale_y(tick)}" x2="{ line_calc_group_x(0)+5}" y2="{line_scale_y(tick)}" />
        <text class="ticks" x="{line_calc_group_x(0)-60}" y="{line_scale_y(tick)+7}">{tick}</text>
    {/each}
</svg>
</div>

<!-- Pie chart -->
<div class="pie_out box" style="width: {line_width}px; height: {line_height}px; position: relative;">
    <text x=100 y=20 style="font-size: 25px; font-style: bold; position: absolute; left: 50px;">Participants per Season</text>
    <text x=50 y=100 style="font-size: 20px; position: absolute; left: 35px; top: 120px;">Summer</text>
    <text x=350 y=100 style="font-size: 20px; position: absolute; left: 300px; top: 100px;">Winter</text>
    <div class="piechart"><!-- {total}, {winter}, {deg_border} --></div>
</div>
</div>

<!-- class .   id # -->
<style>
    .box {
        float: left;
    }
    .piechart {
        width: 200px;
        height: 200px;
        border-radius: 50%;
        background-image: conic-gradient(
            rgb(112, 207, 238) 59.31deg,
            rgb(225, 140, 74) 0 
        );
        margin-top: 110px;
        margin-bottom: 100px;
        margin-left: 130px;
        margin-right: 130px;
    }
    .bar {
        stroke: green;
        stroke-width: 13;
    }
    #x_ticks{
        writing-mode: vertical-lr;
    }
    .tick{
        stroke: black;
        stroke-width: 2;

    }
    .axis{
        stroke: black;
        stroke-width: 2;
    }
    svg, .pie_out {
        border: 1px;
        border-style: solid;
        border-color: gray;
    }
    circle {
        fill: rgb(32, 178, 95);
        fill-opacity: 1;
    }
</style>

