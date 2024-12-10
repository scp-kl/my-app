<script lang="ts">    
    const { data } = $props();

    import DoubleRangeSlider from './DoubleRangeSlider.svelte';
	import RangeSlider from 'svelte-range-slider-pips'
	

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

    let filetered_data = $derived(apply_filter(data.olymCSV, [year_min, year_max, checked_women, checked_men,
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
        console.log(games_set)
        return {filtered: output, distinct: distinct_set, games: games_set};
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
            <div style="margin: 3px;">
                Select the Sports Groups:
                <div style="margin-right: 2em;"><input type="checkbox" bind:checked={checked_group1} /> Group 1 </div>
                <div style="margin-right: 2em;"><input type="checkbox" bind:checked={checked_group2} /> Group 2 </div>
                <div style="margin-right: 2em;"><input type="checkbox" bind:checked={checked_group3} /> Group 3 </div>
                <div style="margin-right: 2em;"><input type="checkbox" bind:checked={checked_group4} /> Group 4 </div>
                <div style="margin-right: 2em;"><input type="checkbox" bind:checked={checked_group5} /> Group 5 </div>
                <div style="margin-right: 2em;"><input type="checkbox" bind:checked={checked_group6} /> Group 6 </div>
                <div style="margin-right: 2em;"><input type="checkbox" bind:checked={checked_group7} /> Group 7 </div>
                <div style="margin-right: 2em;"><input type="checkbox" bind:checked={checked_group8} /> Group 8 </div>
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
        
    </div><!-- topL -->
    <div class="item3"><!-- topM -->

    </div><!-- end topM -->
    <div class="item4"><!-- topR -->

    </div><!-- end topR -->
    <div class="item5"><!-- botL -->

    </div><!-- end botL -->
    <div class="item6"><!-- botR -->

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

