<h1>Survey of the smartphone usage per age</h1>
<!--<p>Visit <a href="https://svelte.dev/docs/kit">svelte.dev/docs/kit</a> to read the documentation</p>-->
<!-- <div>
    <svg width="200" height="200">
        <ellipse cx="20" cy="100" rx="100" ry="20" />
        <rect x="60" y="140" width="50" height="30" />
        <line x1="80" y1="10" x2="140" y2="50" />
    </svg>
</div> -->



<script>
    const { data } = $props();

    let right_shear = 40
    let bottom_shear = 20

    let x_space = 60
    let y_space = 20

    let height = 640 + y_space + bottom_shear
    let width = 390 + x_space + right_shear

    let margin = 20
    let half = margin / 2

    let x_ticks = [5,10,15,20,25,30,35]
    let y_ticks = [30,60,90,120,150]


    function scale_x (a) { return a * 10 + margin + right_shear}
    function scale_y (a) { return height - (a * 4)  + margin - bottom_shear}
</script>

<svg width="{width}" height="{height}">
    {#each data.phoneCSV as datapoint}
        <circle cx="{scale_x(datapoint.Age)}" cy="{scale_y(datapoint.total_use)}" r="3" />
    {/each}
    <line class="axis" id="x" x1="{half + right_shear}" y1="{height-half - bottom_shear}" x2="{width-half-x_space}" y2="{height-half - bottom_shear}" />
    <line class="axis" id="y" x1="{half + right_shear}" y1="{height-half - bottom_shear}" x2="{half + right_shear}" y2="{half+y_space}" />

    <text x="{width-half-x_space + 3}" y="{height-half + 3 - bottom_shear}">Age</text>
    <text x="{half - 3}" y="{half+y_space - 3}">Smartphone Usage per day (min)</text>

    {#each x_ticks as tick}
        <line class="tick" x1="{scale_x(tick)}" y1="{height-half - bottom_shear-5}" x2="{scale_x(tick)}" y2="{height-half - bottom_shear+5}" />
        <text class="ticks" x="{scale_x(tick)-10}" y="{height-half - bottom_shear+17}">{tick}</text>
    {/each}

    {#each y_ticks as tick}
        <line class="tick" x1="{half + right_shear-5}" y1="{scale_y(tick)}" x2="{half + right_shear+5}" y2="{scale_y(tick)}" />
        <text class="ticks" x="{half + right_shear-35}" y="{scale_y(tick)+7}">{tick}</text>
    {/each}
</svg>

    <!-- class .   id # -->
<style>
    .tick{
        stroke: black;
        stroke-width: 2;

    }
    .axis{
        stroke: black;
        stroke-width: 2;
    }
    svg {
        border: 1px;
        border-style: solid;
        border-color: gray;
    }
    circle {
        fill: green;
        fill-opacity: 1;
    }
</style>

