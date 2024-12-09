<script>    
    const { data } = $props();

    let year_slider_min = 1896;
    let year_slider_max = 2016;
    
</script>




<div style="margin-bottom: 10px;">
    <text style="font-size: 30px;font-style: bold;">Olympic Data</text>
    <text style="margin-left: 20px;">Source: <a href="https://www.kaggle.com/datasets/bhanupratapbiswas/olympic-data">Kaggle</a></text>
    <text style="margin-left: 20px;"><a href="./oldDraft">Old Page</a></text>
</div>


<div class="grid-container" style="height:90vh;">
    <div class="item1">left</div>
    <div class="item2">topL</div>
    <div class="item3">topM</div>  
    <div class="item4">topR</div>
    <div class="item5">botL</div>
    <div class="item6">botR</div>
</div>

<!-- class .   id # -->
<style>
    .item1 { grid-area: left; }
    .item2 { grid-area: topL; }
    .item3 { grid-area: topM; }
    .item4 { grid-area: topR; }
    .item5 { grid-area: botL; }
    .item6 { grid-area: botR; }
    .grid-container > div {
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
    }
    :global(body) {
        background-color: lightgrey;
    }


</style>

