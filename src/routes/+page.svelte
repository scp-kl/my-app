<h1>Welcome to my Dashboard</h1>
<!--<p>Visit <a href="https://svelte.dev/docs/kit">svelte.dev/docs/kit</a> to read the documentation</p>-->
<div>
    <svg width="200" height="200">
        <ellipse cx="20" cy="100" rx="100" ry="20" />
        <rect x="60" y="140" width="50" height="30" />
        <line x1="80" y1="10" x2="140" y2="50" />
    </svg>
</div>

<style>
    svg {
        background-color: #c2c2b6
    }
    line {
    stroke: pink;
    stroke-width: 5;
    }
    ellipse {
    fill: steelblue;
    }
    rect {
    fill: grey;
    }
</style>