<script lang="ts">    
    const { data } = $props();

    import DoubleRangeSlider from './DoubleRangeSlider.svelte';
	import RangeSlider from 'svelte-range-slider-pips'
	

    let year_slider_min = $state(0);
    let year_slider_max = $state(1);
    let year_min = $derived(1896 + ((2016-1896) * year_slider_min));
    let year_max = $derived(1896 + ((2016-1896) * year_slider_max));
    let checked_men = $state(false)
    let checked_women = $state(false)
    let checked_summer = $state(false)
    let checked_winter = $state(false)

    const nice = (d:Number) => {
		if (!d && d !== 0) return '';
		return d.toFixed(0);
	}
    
</script>




<div style="margin-bottom: 10px;">
    <text style="font-size: 30px;font-weight: bold;">Olympic Data</text>
    <text style="margin-left: 20px;">Source: <a href="https://www.kaggle.com/datasets/bhanupratapbiswas/olympic-data">Kaggle</a></text>
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
		
		<!-- <RangeSlider values={[11]} /> -->
	</div>
            </div>
        </div>
        <div style="">
            <div style="margin: 3px;">
                Select the Gender:<br>
                <span style="margin-right: 2em;"><input type="checkbox" bind:checked={checked_men} /> m </span>
                <span><input type="checkbox" bind:checked={checked_women} /> f </span>
               
            </div>
        </div>
        <div style="">
            <div style="margin: 3px;">
                <input type="checkbox" bind:checked={checked_men} /><br>
                {checked_men}
            </div>
        </div>
        <div style="">
                test
        </div>
        <div style="">
            test
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
        justify-content: space-between;
    }
    .item1 > div {
        border-bottom: 1px solid black;
        border-top: none;
        border-left: none;
        border-right: none;
        flex-grow: 1;
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

