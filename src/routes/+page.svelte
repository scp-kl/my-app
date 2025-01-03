<script lang="ts">    
    const { data } = $props();

    import DoubleRangeSlider from './DoubleRangeSlider.svelte';
	import RangeSlider from 'svelte-range-slider-pips'
    import { scaleLinear } from 'd3-scale';
	
    let bottom_dict = new Map();
    let year_slider_min = $state(0);
    let year_slider_max = $state(1);
    let year_min = $derived(1896 + ((2016-1896) * year_slider_min));
    let year_max = $derived(1896 + ((2016-1896) * year_slider_max));
    let checked_men = $state(true)
    let checked_women = $state(true)
    let checked_summer = $state(true)
    let checked_winter = $state(true)
    let checked_group1 = $state(true)
    let checked_group2 = $state(true)
    let checked_group3 = $state(true)
    let checked_group4 = $state(true)
    let checked_group5 = $state(true)
    let checked_group6 = $state(true)
    let checked_group7 = $state(true)
    let checked_group8 = $state(true)

    let filetered_data = $derived(update_after_selection(data.olymCSV, [year_min, year_max, checked_women, checked_men,
        checked_group1, checked_group2, checked_group3, checked_group4, checked_group5, checked_group6, checked_group7, 
        checked_group8, checked_summer, checked_winter]))

    const nice = (d:Number) => {
		if (!d && d !== 0) return '';
		return d.toFixed(0);
	}

    function check_gender (point){
        return ((checked_women && point.Sex == "F") || (checked_men && point.Sex == "M"));
    }

    function check_type (point){
        //todo: implement
        return true;
    }

    function check_season (point){
        return ((checked_summer && point.Season == "Summer") || (checked_winter && point.Season == "Winter"));
    }

    function apply_filter (unfiltered_data, ui){
        let output : any[] = [];
        let distinct_set = new Set();
        let games_set = new Set();
        unfiltered_data.forEach(point => {
            if (year_min <= point.Year && year_max >= point.Year &&
                check_gender(point) && check_type(point) && check_season(point)
            ){
                output.push(point);
                distinct_set.add(point.ID)
                games_set.add(point.Games)
            }
        });
        //console.log(unfiltered_data, output)
        //console.log(games_set)
        return {filtered: output, distinct: distinct_set, games: games_set};
    }

    const scale_bl_x = scaleLinear().domain([0,2000]).range(200,10000)

    function update_after_selection(unfiltered_data, ui){
        let res = apply_filter(unfiltered_data, ui);
        calc_bottom(res);
        return res;
    }

    //-------------------------------------------------------------------------
    // bottom
    //-------------------------------------------------------------------------
    
    

    function calc_bottom(in_data){
        let num_x_ticks = 12.0
        let num_x_vals = in_data.games.size
        let vals_per_tick = num_x_vals / num_x_ticks
        vals_per_tick = Math.floor(vals_per_tick)
        let direct_x = vals_per_tick * num_x_ticks
        let missing_x = num_x_vals - direct_x

        let values = Array.from(in_data.games)
        values.sort()

        let num_m = []
        let num_w = []
        let num_1 = []
        let num_2 = []
        let num_3 = []
        let num_4 = []
        let num_5 = []
        let num_6 = []
        let num_7 = []
        let num_8 = []

        let x_comp = []
        let x_ticks = []
        let last_max = -1
        for (var i = 0; i < num_x_ticks; i++){
            let min = values[last_max+1]
            let max_i = last_max + vals_per_tick
            if (i < missing_x){
                max_i += 1;
            }
            let max = "" + values[max_i];
            last_max = max_i;
            var sub_mx = max.substring(0,4)
            x_comp.push(sub_mx);
            let composed = min + " - " + max;
            x_ticks.push(composed);

            num_1.push(0)
            num_2.push(0)
            num_3.push(0)
            num_4.push(0)
            num_5.push(0)
            num_6.push(0)
            num_7.push(0)
            num_8.push(0)
            num_m.push(0)
            num_w.push(0)
        }

        in_data.filtered.forEach((element) => {
            for (var i = 0; i < num_x_ticks; i++){
                if (element.Year <= x_comp[i]){
                    if (element.Sex == "M"){
                        num_m[i] = num_m[i] + 1;
                    }
                    else {
                        num_w[i] = num_w[i] + 1;
                    }

                    if (element.Group == 1){
                        num_1[i] = num_1[i] + 1
                    }
                    else if (element.Group == 2){
                        num_2[i] = num_2[i] + 1
                    }
                    else if (element.Group == 3){
                        num_3[i] = num_3[i] + 1
                    }
                    else if (element.Group == 4){
                        num_4[i] = num_4[i] + 1
                    }
                    else if (element.Group == 5){
                        num_5[i] = num_5[i] + 1
                    }
                    else if (element.Group == 6){
                        num_6[i] = num_6[i] + 1
                    }
                    else if (element.Group == 7){
                        num_7[i] = num_7[i] + 1
                    }
                    else if (element.Group == 8){
                        num_8[i] = num_8[i] + 1
                    }

                    break;
                }
            }
        });

        for (i = 0; i < num_x_ticks; i++){
            var divisor = vals_per_tick
            if (i < missing_x){
                divisor++
            }
            num_m[i] /= divisor;
            num_w[i] /= divisor;

            let sum = num_1[i] + num_2[i] + num_3[i] + num_4[i] + num_5[i] + num_6[i] + num_7[i] + num_8[i];
            num_1[i] /= sum;
            num_2[i] /= sum;
            num_3[i] /= sum;
            num_4[i] /= sum;
            num_5[i] /= sum;
            num_6[i] /= sum;
            num_7[i] /= sum;
            num_8[i] /= sum;
        }

        bottom_dict.set("1", num_1);
        bottom_dict.set("2", num_2);
        bottom_dict.set("3", num_3);
        bottom_dict.set("4", num_4);
        bottom_dict.set("5", num_5);
        bottom_dict.set("6", num_6);
        bottom_dict.set("7", num_7);
        bottom_dict.set("8", num_8);
        bottom_dict.set("m", num_m);
        bottom_dict.set("w", num_w);
        bottom_dict.set("x", x_ticks);


        //console.log(bottom_dict)
    }

    
</script>




<div style="margin-bottom: 10px;">
    <text style="font-size: 30px;font-weight: bold;">Olympic Data</text>
    <text style="margin-left: 20px;">Source: 
        <a href="https://www.kaggle.com/datasets/bhanupratapbiswas/olympic-data">Kaggle</a></text>
    <text style="margin-left: 20px;"><a href="./oldDraft">Old Page</a></text>
</div>


<div class="grid-container" style="height:90vh; width: 99vw;">
    <div class="item1" style="font-size: 17px; font-weight: bold;"><!-- left -->
        <div style="">
            <div style="margin: 3px;">
                Select the Sports Groups:
                <div style="margin-right: 2em;"><input type="checkbox" bind:checked={checked_group1} /> Team Sports </div>
                <div style="margin-right: 2em;"><input type="checkbox" bind:checked={checked_group2} /> Racquet Sports </div>
                <div style="margin-right: 2em;"><input type="checkbox" bind:checked={checked_group3} /> Combat Sports </div>
                <div style="margin-right: 2em;"><input type="checkbox" bind:checked={checked_group4} /> Water Sports </div>
                <div style="margin-right: 2em;"><input type="checkbox" bind:checked={checked_group5} /> Winter Sports </div>
                <div style="margin-right: 2em;"><input type="checkbox" bind:checked={checked_group6} /> 
                    Track and Field <br><div style="text-indent:1.6em;">Sports</div> </div>
                <div style="margin-right: 2em;"><input type="checkbox" bind:checked={checked_group7} /> 
                    Gymnastics and <br><div style="text-indent:1.6em;">Acrobatic Sports</div>  </div>
                <div style="margin-right: 2em;"><input type="checkbox" bind:checked={checked_group8} /> Remaining Sports </div>
            </div>
        </div>
        <div style="height:10vh;">
            <div style="margin: 3px;">
                Select the year range:
                <div style="margin: 5px 10px;">
                    <DoubleRangeSlider bind:start={year_slider_min} bind:end={year_slider_max}/>
                </div>
                <div class="labels">
                    <span class="label">{nice(year_min)}</span>
                    <span class="label">{nice(year_max)}</span>
                </div>
                <div class="slider">
	            </div>
            </div>
        </div>
        <div style="">
            <div style="margin: 3px;">
                Select the Gender:<br>
                <span style="margin-right: 2em;"><input type="checkbox" bind:checked={checked_men} /> M </span>
                <span><input type="checkbox" bind:checked={checked_women} /> F </span>
            </div>
        </div>
        <div style="">
            <div style="margin: 3px;">
                Select the Games:<br>
                <span style="margin-right: 2em;"><input type="checkbox" bind:checked={checked_summer} /> Summer </span>
                <span><input type="checkbox" bind:checked={checked_winter} /> Winter </span>
            </div>
        </div>
        <div style="">
            Number of Elements: <br>
            {filetered_data.filtered.length} / 70000<br>
            Distinct people: <br>
            {filetered_data.distinct.size} / 35658<br>
            Distinct Games:<br>
            {filetered_data.games.size} / 51
        </div>
    </div><!-- end left -->
    <div class="item2"><!-- topL -->
        <img src="images/top_left.png" style="height: 40vh;" alt="background image" />
    </div><!-- topL -->
    <div class="item3"><!-- topM -->
        <img src="images/top_middle.png" style="height: 40vh;" alt="background image" />
    </div><!-- end topM -->
    <div class="item4"><!-- topR -->
        <img src="images/top_right.png" style="height: 40vh;" alt="background image" />
    </div><!-- end topR -->
    <div class="item5"><!-- botL -->
        <img src="images/bottom_left.png" style="height: 35vh;" alt="background image" />
    </div><!-- end botL -->
    <div class="item6"><!-- botR -->
        Attendancies per sports type (averaged per game)
    </div><!-- end botR -->
</div>

<!-- class .   id # -->
<style>
    * {
        box-sizing: border-box;
    }
    .labels {
        display: flex;
        justify-content: space-between;
    }
    .item1 { 
        grid-area: left;
        display: flex;
        flex-direction: column;
        justify-content: space-around;
        overflow-y: auto;
    }
    .item1 > div {
        /* border-bottom: 1px solid black; */
        border-top: none;
        border-left: none;
        border-right: none;
        /* flex-grow: 1; */
    }
    .item2 { grid-area: topL; }
    .item3 { grid-area: topM; }
    .item4 { grid-area: topR; }
    .item5 { grid-area: botL; }
    .item6 { grid-area: botR; }
    .grid-container > div {/* div elements of the grid */
    background-color: lightgrey;
    }
    .grid-container {
        display: grid;
        grid-template-areas:
            'left topL topL topM topM topR topR'
            'left topL topL topM topM topR topR'
            'left botL botL botL botR botR botR'
            'left botL botL botL botR botR botR';
        gap: 3px;
        background-color: #77797a;
        padding: 3px;
        grid-template-columns: repeat(7, 1fr);
    }
    :global(body) {
        background-color: lightgrey;
    }

    .show {
        border: 1px;
        border-style: solid;
        border-color: greenyellow;
    }

</style>

