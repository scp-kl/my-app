<script lang="ts">
	//import { LOGNAME } from '$env/static/private';
    
    const { data } = $props();

	//import { color, group } from 'd3';
    import DoubleRangeSlider from './DoubleRangeSlider.svelte';
	import RangeSlider from 'svelte-range-slider-pips'
	//import { get } from 'svelte/store';
    //import { scaleLinear } from 'd3-scale';
	
    let sports_types = new Map([["1", "Team"], ["2", "Racquet"], ["3", "Combat"], ["4", "Water"], ["5", "Winter"], ["6", "Track/Field"], 
            ["7", "Gymnast./Acrob."], ["8", "Remaining"]]);

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
        return ((checked_group1 && point.Group == "1") || (checked_group2 && point.Group == "2") || (checked_group3 && point.Group == "3") || 
                (checked_group4 && point.Group == "4") || (checked_group5 && point.Group == "5") || (checked_group6 && point.Group == "6") || 
                (checked_group7 && point.Group == "7") || (checked_group8 && point.Group == "8"));
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
                check_gender(point) && check_season(point)
            ){
                output.push(point);
                distinct_set.add(point.ID)
                games_set.add(point.Games)
            }
        });
        //console.log(unfiltered_data, output)
        //console.log(games_set)
        let out = new Map()
        out.set("filtered", output)
        out.set("distinct", distinct_set)
        out.set("games", games_set)
        return out
    }

    //const scale_bl_x = scaleLinear().domain([0,2000]).range(200,10000)

    function update_after_selection(unfiltered_data, ui){
        let res = apply_filter(unfiltered_data, ui);
        res = calc_bottom(res);
        res = calc_top(res)
        //console.log(res)
        return res;
    }



    //-------------------------------------------------------------------------
    // top
    //-------------------------------------------------------------------------

    
    function calc_top(in_data){
        let top_l = new Map();
        let top_m = new Map();
        let top_r = new Map();


        const l_med = new Map(); const l_num = new Map();
        const m_age = new Map(); const m_num = new Map(); const m_wei = new Map(); const m_hei = new Map();
        const r_w_med = new Map(); const r_w_num = new Map(); const r_m_med = new Map(); const r_m_num = new Map(); const r_num = new Map(); const r_age = new Map();

        in_data.get("filtered").forEach((element) => {
            if (check_type(element)){
                l_num.set(element.NOC, (l_num.get(element.NOC) ?? 0) +1);
            }

            if (element.Age > 0 && element.Weight > 0 && element.Height > 0){
                m_age.set(element.Group, (m_age.get(element.Group) ?? 0) + Number(element.Age));
                m_hei.set(element.Group, (m_hei.get(element.Group) ?? 0) + Number(element.Height));
                m_wei.set(element.Group, (m_wei.get(element.Group) ?? 0) + Number(element.Weight));
                m_num.set(element.Group, (m_num.get(element.Group) ?? 0) + 1);
            }

            if (element.Medal != "" && element.Medal != null){
                if (check_type(element)){
                    let to_add = 1;
                    if (element.Medal == "Silver") {to_add = 2;}
                    else if (element.Medal == "Gold") {to_add = 3;}
                    l_med.set(element.NOC, (l_med.get(element.NOC) ?? 0) + to_add);
                }


                r_num.set(element.Group, (r_num.get(element.Group) ?? 0) +1);
                r_age.set(element.Group, (r_age.get(element.Group) ?? 0) + Number(element.Age));
                
                if (element.Sex == "F"){
                    r_w_med.set(element.Group, (r_w_med.get(element.Group) ?? 0) +1);
                }
                else {
                    r_m_med.set(element.Group, (r_m_med.get(element.Group) ?? 0) +1);
                }
            }

            if (element.Sex == "F"){
                r_w_num.set(element.Group, (r_w_num.get(element.Group) ?? 0) +1);
            }
            else {
                r_m_num.set(element.Group, (r_m_num.get(element.Group) ?? 0) +1);
            }
        });

        //--------------
        // top left
        //--------------

        let keyset = l_num.keys();
        let sort_abs = []
        let sort_rel = []
        keyset.forEach((element) => {
            let num = l_num.get(element);
            let med = l_med.get(element) ?? 0;
            let rel = med / num;

            sort_abs.push({num: med, nat: element});
            sort_rel.push({num: rel, nat: element});
        })
        sort_abs.sort((a,b) => b.num - a.num)
        sort_rel.sort((a,b) => b.num - a.num)

        top_l.set("best_rel", [sort_rel[0].nat, sort_rel[1].nat, sort_rel[2].nat])
        top_l.set("best_abs", [sort_abs[0].nat, sort_abs[1].nat, sort_abs[2].nat])
        let len = sort_abs.length - 1
        top_l.set("worst_rel", [sort_rel[len - 0].nat, sort_rel[len - 1].nat, sort_rel[len - 2].nat])
        top_l.set("worst_abs", [sort_abs[len - 0].nat, sort_abs[len - 1].nat, sort_abs[len - 2].nat])



        //--------------
        // top middle
        //--------------
        
        let groups = sports_types.keys();
        let top_m_max_age = 0;
        let top_m_max_hei = 0;
        let top_m_max_wei = 0;
        let top_m_min_age = 500;
        let top_m_min_hei = 500;
        let top_m_min_wei = 500;

        groups.forEach(element => {
            let num = m_num.get(element) ?? 0;
            let tmp = new Map([["sport", sports_types.get(element)], ["age", 0], ["hei", 0], ["wei", 0]]);
            if (num > 0){
                let age = m_age.get(element);
                let hei = m_hei.get(element);
                let wei = m_wei.get(element);

                age = age/num;
                hei = hei/num;
                wei = wei/num;

                tmp = new Map([["sport", sports_types.get(element)], ["age", age], ["hei", hei], ["wei", wei]]);

                if (age < top_m_min_age){
                    top_m_min_age = age;
                }
                if (age > top_m_max_age){
                    top_m_max_age = age;
                }
                if (wei < top_m_min_wei){
                    top_m_min_wei = wei;
                }
                if (wei > top_m_max_wei){
                    top_m_max_wei = wei;
                }
                if (hei < top_m_min_hei){
                    top_m_min_hei = hei;
                }
                if (hei > top_m_max_hei){
                    top_m_max_hei = hei;
                }

        //console.log(val)
            }
            top_m.set(element, tmp);
            //console.log(tmp)
        });
        //console.log(top_m)
        var top_m_stat = new Map([
            ["age_max", top_m_max_age], ["age_min", top_m_min_age], ["age_diff", top_m_max_age - top_m_min_age],
            ["hei_max", top_m_max_hei], ["hei_min", top_m_min_hei], ["hei_diff", top_m_max_hei - top_m_min_hei],
            ["wei_max", top_m_max_wei], ["wei_min", top_m_min_wei], ["wei_diff", top_m_max_wei - top_m_min_wei]
        ]);
        //console.log(top_m_stat)

        //--------------
        // top right
        //--------------

        let woman = []
        let men = []
        let age = []
        groups = sports_types.keys();
        groups.forEach(element => {
            let gr = sports_types.get(element)
            let w_score = 0;
            let w_num = r_w_num.get(element) ?? 0;
            if (w_num > 0) {
                let w_med = r_w_med.get(element) ?? 0;
                w_score = w_med / w_num;
            }
            woman.push({"group": gr, "score": w_score})

            let m_score = 0;
            let m_num = r_m_num.get(element) ?? 0;
            if (m_num > 0) {
                let m_med = r_m_med.get(element) ?? 0;
                m_score = m_med / m_num;
            }
            men.push({"group": gr, "score": m_score})

            let a_score = 0;
            let a_num = r_num.get(element) ?? 0;
            if (a_num > 0) {
                let a_med = r_age.get(element) ?? 0;
                a_score = a_med / a_num;
            }
            age.push({"group": gr, "score": a_score})
        })
        woman.sort((a,b) => b.score - a.score)
        men.sort((a,b) => b.score - a.score)
        age.sort((a,b) => b.score - a.score)

        top_r.set("women", [woman[0].group, woman[1].group, woman[2].group])
        top_r.set("men", [men[0].group, men[1].group, men[2].group])
        top_r.set("old", [age[0].group, age[1].group, age[2].group])
        len = age.length - 1
        top_r.set("young", [age[len].group, age[len - 1].group, age[len - 2].group])

        //console.log(top_r)

        in_data.set("top_l", top_l)
        in_data.set("top_m", top_m)
        in_data.set("top_m_stat", top_m_stat)
        in_data.set("top_r", top_r)
        return in_data
    }

    function transform_top_m (row, col) {
        let val = ((row - 1) * 3) + col;
        if (val > 5){
            val = val - 1;
        }

        return val;
    }

    function top_m_age (input_data) {
        let tmp = input_data - filetered_data.get("top_m_stat").get("age_min");
        tmp = tmp / filetered_data.get("top_m_stat").get("age_diff");
        return tmp;
    }

    function top_m_hei (input_data) {
        let tmp = input_data - filetered_data.get("top_m_stat").get("hei_min");
        tmp = tmp / filetered_data.get("top_m_stat").get("hei_diff");
        //console.log("hei", tmp+1)
        return 1 + tmp;
    }

    function top_m_wei (input_data) {
        let tmp = input_data - filetered_data.get("top_m_stat").get("wei_min");
        tmp = tmp / filetered_data.get("top_m_stat").get("wei_diff");
        //console.log("wei", tmp+1)
        return 1 + tmp;
    }


    //-------------------------------------------------------------------------
    // bottom
    //-------------------------------------------------------------------------

    let bot_num_x_ticks = 12.0
    let bot_ticks = Array(bot_num_x_ticks).fill(0).map((_, i) => i)
    //console.log(bot_ticks)

    function calc_bottom(in_data){
        let bottom_dict = new Map();


        let bot_num_x_ticks = 12.0
        let num_x_vals = in_data.get("games").size
        let vals_per_tick = num_x_vals / bot_num_x_ticks
        vals_per_tick = Math.floor(vals_per_tick)
        let direct_x = vals_per_tick * bot_num_x_ticks
        let missing_x = num_x_vals - direct_x

        let values = Array.from(in_data.get("games"))
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
        for (var i = 0; i < bot_num_x_ticks; i++){
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

        in_data.get("filtered").forEach((element) => {
            for (var i = 0; i < bot_num_x_ticks; i++){
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

        let bot_l_max = 0;

        for (i = 0; i < bot_num_x_ticks; i++){
            var divisor = vals_per_tick
            if (i < missing_x){
                divisor++
            }
            num_m[i] /= divisor;
            num_w[i] /= divisor;

            if (bot_l_max < num_w[i]){
                bot_l_max = num_w[i]
            }
            if (bot_l_max < num_m[i]){
                bot_l_max = num_m[i]
            }

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

        for (i = 0; i < bot_num_x_ticks; i++){
            num_2[i] += num_1[i];
            num_3[i] += num_2[i];
            num_4[i] += num_3[i];
            num_5[i] += num_4[i];
            num_6[i] += num_5[i];
            num_7[i] += num_6[i];
            num_8[i] += num_7[i];
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
        bottom_dict.set("max", bot_l_max)


        //console.log(bottom_dict)
        in_data.set("bottom", bottom_dict)
        return in_data
    }

    let bottom_height = 70;
    let bottom_width = 72;
    let bottom_top = 27;
    let bottom_left = 8;

    /**
	 * @param {any} a
	 */
     function bottom_scale_x (a) { return a * (bottom_width / (bot_num_x_ticks + 1)) + bottom_left}

    /**
	 * @param {any} a
	 */
     function l_bottom_scale_x (a) { return a * ((95 - bottom_left) / (bot_num_x_ticks + 1)) + bottom_left}

    /**
     * @param {any} a
     */
    function bottom_scale_y (a) { return 100 - (a * bottom_height) - bottom_top}

    //let bot_color = ["red", "blue", "green", "orange", "grey", "yellow", "pink", "brown"]
    //let bot_color = ["#FFCCFF", "#A3D9FF", "#B2F0B1", "#FFEB99", "#FFD1E6", "#FFBC99", "#E2A9FF", "#FFB3B3"]
    let bot_color = [
    "#FF8080", // Slightly darker Light Red
    "#FF99CC", // Slightly darker Light Pink
    "#80BFFF", // Slightly darker Light Blue
    "#99E699", // Slightly darker Light Green
    "#FFD966", // Slightly darker Light Yellow
    "#FFB3D9", // Slightly darker Pastel Lavender
    "#FF9966", // Slightly darker Light Coral
    "#D18CFF"  // Slightly darker Light Violet
    ]
    let men_color = bot_color[2];
    let women_color = bot_color[0];
    let comp_color = bot_color[6];
    let grey_color = "grey";
    //console.log(filetered_data.get("bottom").get(1+""))

    function scale_top_m_color (a) {
        let red = 255;
        let green = 153;
        let blue = 102;

        let r_diff = ((red +((137 - red) * a))+"").split(".")[0];
        let g_diff = ((green + ((137 - green) * a))+"").split(".")[0];
        let b_diff = ((blue + ((137 - blue) * a))+"").split(".")[0];

        let res = "rgb(" + (r_diff) + ", " + g_diff + ", " + b_diff + ")";
        console.log(a + ": " + res)/* TODO: delete */
        return res
    }
    
</script>




<div style="margin-bottom: 10px;">
    <text style="font-size: 30px;font-weight: bold;">Olympic Data</text>
    <text style="margin-left: 20px;">Source: 
        <a href="https://www.kaggle.com/datasets/bhanupratapbiswas/olympic-data">Kaggle</a></text>
    <text style="margin-left: 20px;"><a href="./oldDraft">Old Page</a></text>
</div>


<div class="grid-container" style="height:90vh; width: 99vw;">
    <div class="item1" style=""><!-- left -->
        <div class="sidebar">
            <div class="text_l" style="margin: 3px;">
                <div style="text-align: center; margin-bottom: 0.5sem;">
                    Select the Sports Groups:
                </div>
                <div class="text_l uistack tooltipped" style="">
                    <input type="checkbox" id="group1" bind:checked={checked_group1} /> 
                    <label for="group1"> Team Sports </label>
                    <div class="tooltip tooltip-right">
                        <ul class="list_tool">
                            <li>Football</li><li>Handball</li><li>Hockey</li><li>Ice Hockey</li><li>Rugby Sevens</li>
                            <li>Water Polo</li><li>Lacrosse</li><li>Basketball</li><li>Volleyball</li><li>Rugby</li>
                            <li>Softball</li><li>Baseball</li><li>Cricket</li><li>Polo</li><li>Beach Volleyball</li>
                            <li>Polo</li>
                        </ul>
                    </div>
                </div>
                <div class="text_l uistack tooltipped" style="">
                    <input type="checkbox" id="group2" bind:checked={checked_group2} /> 
                    <label for="group2">Racquet Sports 
                    </label>
                    <div class="tooltip tooltip-right">
                        <ul class="list_tool">
                            <li>Tennis</li><li>Badminton</li><li>Table Tennis</li><li>Croquet</li><li>Jeu De Paume</li>
                            <li>Racquets</li>
                        </ul>
                    </div>
                </div>
                <div class="text_l uistack tooltipped" style=""><input type="checkbox" id="group3" bind:checked={checked_group3} /> 
                    <label for="group3">Combat Sports 
                    </label>
                    <div class="tooltip tooltip-right">
                        <ul class="list_tool">
                            <li>Judo</li><li>Taekwondo</li><li>Boxing</li><li>Wrestling</li><li>Fencing</li>
                        </ul>
                    </div>
                </div>
                <div class="text_l uistack tooltipped" style=""><input type="checkbox" id="group4" bind:checked={checked_group4} /> 
                    <label for="group4">Water Sports </label>
                    <div class="tooltip tooltip-right">
                        <ul class="list_tool">
                            <li>Sailing</li><li>Swimming</li><li>Diving</li><li>Synchronized Swimming</li><li>Canoeing</li>
                            <li>Rowing</li>
                        </ul>
                    </div>
                </div>
                <div class="text_l uistack tooltipped" style=""><input type="checkbox" id="group5" bind:checked={checked_group5} /> 
                    <label for="group5">Winter Sports </label>
                    <div class="tooltip tooltip-right">
                        <ul class="list_tool">
                            <li>Biathlon</li><li>Ski Jumping</li><li>Snowboarding</li><li>Alpine Skiing</li><li>Freestyle Skiing</li>
                            <li>Cross Country Skiing</li><li>Bobsleigh</li><li>Skeleton</li><li>Luge</li><li>Nordic Combined</li>
                            <li>Curling</li>
                        </ul>
                    </div>
                </div>
                <div class="text_l uistack tooltipped" style="">
                    <input type="checkbox" id="group6" bind:checked={checked_group6} /> 
                    <label for="group6">Track and Field Sports</label>
                    <div class="tooltip tooltip-right">
                        <ul class="list_tool">
                            <li>Athletics</li><li>Weightlifting</li><li>Triathlon</li><li>Cycling</li><li>Speed Skating</li>
                            <li>Short Track Speed Skating</li><li>Modern Pentathlon</li>
                        </ul>
                    </div>
                </div>
                <div class="text_l uistack tooltipped" style=""><input type="checkbox" id="group7" bind:checked={checked_group7} /> 
                    <label for="group7">Gymnastics and Acrobatic Sports</label>  
                    <div class="tooltip tooltip-right">
                        <ul class="list_tool">
                            <li>Gymnastics</li><li>Rhythmic Gymnastics</li><li>Trampolining</li><li>Figure Skating</li>
                        </ul>
                    </div>
                </div>
                <div class="text_l uistack tooltipped" style=""><input type="checkbox" id="group8" bind:checked={checked_group8} /> 
                    <label for="group8">Remaining Sports </label>
                    <div class="tooltip tooltip-right">
                        <ul class="list_tool">
                            <li>Art Competitions</li><li>Military Ski Patrol</li><li>Alpinism</li><li>Tug-Of-War</li><li>Motorboating</li>
                            <li>Basque Pelota</li><li>Roque</li><li>Golf</li><li>Archery</li><li>Shooting</li>
                            <li>Equestrianism</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
        <div  class="text_l sidebar" style="border: none">
            <div class="left_stats">
                Number of Elements: <br>
                {filetered_data.get("filtered").length} / 70000
            </div>
            <div class="left_stats">
                Distinct People: <br>
                {filetered_data.get("distinct").size} / 35658
            </div>
            <div class="left_stats">
                Distinct Games:<br>
                {filetered_data.get("games").size} / 51
            </div>
        </div>
        <div class="sidebar" style="height:10vh;">
            <div class="text_l" style="margin: 3px; text-align: center;">
                Select the year range:
                <div style="margin: 5px 10px;">
                    <DoubleRangeSlider bind:start={year_slider_min} bind:end={year_slider_max}/>
                </div>
                <div class="labels">
                    <span class="label text_l">{nice(year_min)}</span>
                    <span class="label text_l">{nice(year_max)}</span>
                </div>
                <div class="slider">
	            </div>
            </div>
        </div>
        <div class="sidebar" style=" text-align: center;">
            <div class="text_l" style="margin: 3px;">
                Select the Gender:<br>
                <span style="margin-right: 2em;"><input type="checkbox" bind:checked={checked_men} /> M </span>
                <span><input type="checkbox" bind:checked={checked_women} /> F </span>
            </div>
        </div>
        <div class="text_l sidebar" style=" text-align: center;">
            <div style="margin: 3px;">
                Select the Season:<br>
                <span style="margin-right: 1.5em;"><input type="checkbox" bind:checked={checked_summer} /> Summer </span>
                <span><input type="checkbox" bind:checked={checked_winter} /> Winter </span>
            </div>
        </div>
    </div><!-- end left -->
    <div class="item2"><!-- topL -->
        <div style="height: 49%; width: 100%; padding: 3px; font-size: 17px; font-weight: bold; ">
            <div class="heading" style="">
                Best Nations:
            </div>
            <div class="top_pic" style="">
                Absolute:<br>
                <img class="podium" src="images/best_podium.png" style="width: 95%;" alt="background image" />
                <div style="position: absolute; left: 43%; bottom: 55%;"> {filetered_data.get("top_l").get("best_abs")[0] ?? 0}</div>
                <div style="position: absolute; left: 12%; bottom: 41%;"> {filetered_data.get("top_l").get("best_abs")[1] ?? 0}</div>
                <div style="position: absolute; left: 73%; bottom: 35%;"> {filetered_data.get("top_l").get("best_abs")[2] ?? 0}</div>
            </div>
            <div class="top_pic" style="">
                Relative:<br>
                <img class="podium" src="images/best_podium.png" style="width: 95%;" alt="background image" />
                <div style="position: absolute; left: 43%; bottom: 55%;"> {filetered_data.get("top_l").get("best_rel")[0] ?? 0}</div>
                <div style="position: absolute; left: 12%; bottom: 41%;"> {filetered_data.get("top_l").get("best_rel")[1] ?? 0}</div>
                <div style="position: absolute; left: 73%; bottom: 35%;"> {filetered_data.get("top_l").get("best_rel")[2] ?? 0}</div>
            </div>
        </div>
        <div style="height: 49%; width: 100%; padding: 3px; font-size: 17px; font-weight: bold;">
            <div class="heading" style="padding: 1%">
                Worst Nations:
            </div>
            <div class="top_pic" style="">
                Absolute:<br>
                <img class="podium2" src="images/worst_podium.png" style="width: 95%;" alt="background image" />
                <div style="position: absolute; left: 43%; bottom: 22%;"> {filetered_data.get("top_l").get("worst_abs")[0] ?? 0}</div>
                <div style="position: absolute; left: 12%; bottom: 41%;"> {filetered_data.get("top_l").get("worst_abs")[1] ?? 0}</div>
                <div style="position: absolute; left: 73%; bottom: 35%;"> {filetered_data.get("top_l").get("worst_abs")[2] ?? 0}</div>
            </div>
            <div class="top_pic" style="">
                Relative:<br>
                <img class="podium2" src="images/worst_podium.png" style="width: 95%;" alt="background image" />
                <div style="position: absolute; left: 43%; bottom: 22%;"> {filetered_data.get("top_l").get("worst_rel")[0] ?? 0}</div>
                <div style="position: absolute; left: 12%; bottom: 41%;"> {filetered_data.get("top_l").get("worst_rel")[1] ?? 0}</div>
                <div style="position: absolute; left: 73%; bottom: 35%;"> {filetered_data.get("top_l").get("worst_rel")[2] ?? 0}</div>
            </div>
        </div>
    </div><!-- topL -->
    <div class="item3"><!-- topM -->
        <div class="top_m_sports heading" style="margin: 0.7%;">
            Comparison of athletes dimensions:
        </div>
        {#each [1,2,3] as row}
        <div class="top_m_outer" style="">
            {#each [1,2,3] as col}
            <div class="mid_pic" style="">
                {#if row == 2 && col == 2}
                <!-- <div class="top_m_sports">Legend</div> -->
                <svg class="" style="margin-top: 3px; left: 3px; position: absolute; transform: translate(-5%, 5%); font-size: 12px;" height="98%" width="98%">

                    <rect style="fill:{scale_top_m_color(0.5)}; width:30%; height:45%; z-index: -50;top:80%;left: 20%;" x="21%" y="33.5%" />
                    
                    <!-- height --><!-- weight -->
                     <line class="axis" x1="20%" x2="20%" y1="15%" y2="85%"/> 
                     <line class="axis" x1="15%" x2="65%" y1="80%" y2="80%"/> 
                     <text x="3%" y="10%" style="font-size: 12px;">height in cm</text>
                     <text x="68%" y="82%" style="font-size: 12px;">weight</text>
                     <text x="68%" y="92%" style="font-size: 12px;">in kg</text>

                     <line class="tick" x1="60%" x2="60%" y1="78%" y2="82%" />
                     <text x="55%" y="93%" style="font-size: 12px;">{(""+filetered_data.get("top_m_stat").get("wei_max")).split(".")[0]}</text>
                     <line class="tick" x1="40%" x2="40%" y1="78%" y2="82%" />
                     <text x="35%" y="93%" style="font-size: 12px;">{(""+filetered_data.get("top_m_stat").get("wei_min")).split(".")[0]}</text>

                     <line class="tick" x1="18%" x2="22%" y1="50%" y2="50%" />
                     <text x="4%" y="54%" style="font-size: 12px;">{(""+filetered_data.get("top_m_stat").get("hei_min")).split(".")[0]}</text>
                     <line class="tick" x1="18%" x2="22%" y1="20%" y2="20%" />
                     <text x="4%" y="24%" style="font-size: 12px;">{(""+filetered_data.get("top_m_stat").get("hei_max")).split(".")[0]}</text>

                    

                    
                    
                    <!-- age -->
                    <!-- <text x="30%" y="28%" style="font-size: 12px;">The colors' border</text>
                    <text x="30%" y="38%" style="font-size: 12px;">signal the age:</text>
                    <text x="30%" y="48%" style="font-size: 12px;">top: {(""+filetered_data.get("top_m_stat").get("age_min")).split(".")[0]}</text>
                    <text x="30%" y="58%" style="font-size: 12px;">bottom: {(""+filetered_data.get("top_m_stat").get("age_max")).split(".")[0]}</text> -->

                    <text x="70%" y="11%" style="">Age:</text>
                    <rect style="height: 1em; width:1em; fill: {scale_top_m_color(0)}" x="70%" y="21%" />
                    <text x="80%" y="30%" style="">{(""+filetered_data.get("top_m_stat").get("age_min")).split(".")[0]}</text>
                    <rect style="height: 1em; width:1em; fill: {scale_top_m_color(1)}" x="70%" y="41%" />
                    <text x="80%" y="50.5%" style="">{(""+filetered_data.get("top_m_stat").get("age_max")).split(".")[0]}</text>
                    
                </svg>
                <img src="images/top_m_man.png" style="position:absolute; width:30%; height:45%; z-index: 50;bottom:15%;left: 17.5%;" alt=""/>
                {:else}
                
                <div class="top_m_sports">{filetered_data.get("top_m").get(transform_top_m(row, col) +"").get("sport")}</div>
                <div class="" style="width: {top_m_wei(filetered_data.get("top_m").get(transform_top_m(row, col) +"").get("wei")) * 20}%;
                    height: {top_m_hei(filetered_data.get("top_m").get(transform_top_m(row, col) +"").get("hei")) * 30}%;
                    margin-left:{(100-(top_m_wei(filetered_data.get("top_m").get(transform_top_m(row, col) +"").get("wei")) * 20))/2}%;
                    margin-top: 5%; position: absolute;">
                    <svg style="width:100%; height:100%; position: absolute; transform: translateX(-50%);">
                        <rect style="fill:{scale_top_m_color(top_m_age(filetered_data.get("top_m").get(transform_top_m(row, col) +"").get("age")))}; width:100%; height:100%" x="0px" y="0px" />
                        <!-- <rect style="fill:{grey_color}; width:100%; 
                            height:{top_m_age(filetered_data.get("top_m").get(transform_top_m(row, col) +"").get("age")) * 100}%" x="0px" y="0px" /> -->
                    </svg>
                    <img class="" src="images/top_m_man.png" width="100%" height="100%" style="top:0px; position: absolute;transform: translateX(-50%);" alt="background image" />
                    
                </div>
             
                {/if}
            </div>
            {/each}
        </div>
        {/each}
    </div><!-- end topM -->
    <div class="item4"><!-- topR -->
        <div class="top_r_outer" style="">
            <div class="heading" style="margin-bottom: 1%;">
                Best Sports to get medals:
            </div>
            <div class="top_pic" style="">
                <div style="font-weight: bold; margin-top: 3%;">For women:</div>
                <div class="top_r_box" style="top: 20%;">
                    <img class="medals" src="images/gold_medal.png" style="" alt="background image" />
                    <text class="top_r_text" style="">{filetered_data.get("top_r").get("women")[0]}</text>
                </div>
                <div class="top_r_box" style=" top: 40%;">
                    <img class="medals" src="images/silver_medal.png" style="" alt="background image" />
                    <text class="top_r_text" style="">{filetered_data.get("top_r").get("women")[1]}</text>
                </div>
                <div class="top_r_box" style="top: 60%;">
                    <img class="medals" src="images/bronze_medal.png" style="" alt="background image" />
                    <text class="top_r_text" style="">{filetered_data.get("top_r").get("women")[2]}</text>
                </div>
            </div>
            <div class="top_pic" style="">
                <div style="font-weight: bold; margin-top: 3%;">For men:</div>
                <div class="top_r_box" style="top: 20%;">
                    <img class="medals" src="images/gold_medal.png" style="" alt="background image" />
                    <text class="top_r_text" style="">{filetered_data.get("top_r").get("men")[0]}</text>
                </div>
                <div class="top_r_box" style=" top: 40%;">
                    <img class="medals" src="images/silver_medal.png" style="" alt="background image" />
                    <text class="top_r_text" style="">{filetered_data.get("top_r").get("men")[1]}</text>
                </div>
                <div class="top_r_box" style="top: 60%;">
                    <img class="medals" src="images/bronze_medal.png" style="" alt="background image" />
                    <text class="top_r_text" style="">{filetered_data.get("top_r").get("men")[2]}</text>
                </div>
            </div>
        </div>
        <div class="top_r_outer" style="">
            <div class="top_pic" style="">
                <div style="font-weight: bold; margin-top: 3%;">For old athletes:</div>
                <div class="top_r_box" style="top: 20%;">
                    <img class="medals" src="images/gold_medal.png" style="" alt="background image" />
                    <text class="top_r_text" style="">{filetered_data.get("top_r").get("old")[0]}</text>
                </div>
                <div class="top_r_box" style=" top: 40%;">
                    <img class="medals" src="images/silver_medal.png" style="" alt="background image" />
                    <text class="top_r_text" style="">{filetered_data.get("top_r").get("old")[1]}</text>
                </div>
                <div class="top_r_box" style="top: 60%;">
                    <img class="medals" src="images/bronze_medal.png" style="" alt="background image" />
                    <text class="top_r_text" style="">{filetered_data.get("top_r").get("old")[2]}</text>
                </div>
            </div>
            <div class="top_pic" style="">
                <div style="font-weight: bold; margin-top: 3%;">For young athletes:</div>
                <div class="top_r_box" style="top: 20%;">
                    <img class="medals" src="images/gold_medal.png" style="" alt="background image" />
                    <text class="top_r_text" style="">{filetered_data.get("top_r").get("young")[0]}</text>
                </div>
                <div class="top_r_box" style=" top: 40%;">
                    <img class="medals" src="images/silver_medal.png" style="" alt="background image" />
                    <text class="top_r_text" style="">{filetered_data.get("top_r").get("young")[1]}</text>
                </div>
                <div class="top_r_box" style="top: 60%;">
                    <img class="medals" src="images/bronze_medal.png" style="" alt="background image" />
                    <text class="top_r_text" style="">{filetered_data.get("top_r").get("young")[2]}</text>
                </div>
            </div>
        </div>
    </div><!-- end topR -->
    <div class="item5"><!-- botL -->
        <div class="heading">
            Attendancies averaged per game: <text style="color: {women_color}">women</text> and <text style="color: {men_color}">men</text>
        </div>
        <svg class="bottpic" style="">
            <line class="axis" id="x" x1="{l_bottom_scale_x(-0.5)}%" y1="{bottom_scale_y(0)}%" x2="{l_bottom_scale_x(bot_num_x_ticks+0.5)}%" y2="{bottom_scale_y(0)}%" />
            <line class="axis" id="y" x1="{l_bottom_scale_x(0)}%" y1="{bottom_scale_y(-0.04)}%" x2="{l_bottom_scale_x(0)}%" y2="{bottom_scale_y(1.025)}%" />

            {#each bot_ticks as i}
                <line class="tick" y1="{bottom_scale_y(-0.02)}%" y2="{bottom_scale_y(0.02)}%" x1="{l_bottom_scale_x(i+1)}%" x2="{l_bottom_scale_x(i+1)}%" />

                <line class="bar" style="stroke: {women_color};" y1="{bottom_scale_y(0)}%" y2="{bottom_scale_y(filetered_data.get("bottom").get("w")[i] / filetered_data.get("bottom").get("max"))}%" 
                        x1="{l_bottom_scale_x(i+1.2)}%" x2="{l_bottom_scale_x(i+1.2)}%" />
                <line class="bar" style="stroke: {men_color};" y1="{bottom_scale_y(0)}%" y2="{bottom_scale_y(filetered_data.get("bottom").get("m")[i] / filetered_data.get("bottom").get("max"))}%" 
                        x1="{l_bottom_scale_x(i+0.8)}%" x2="{l_bottom_scale_x(i+0.8)}%" />



                <text x="{l_bottom_scale_x(i+1.2)}%" y="{bottom_scale_y(-0.02)}%" style="writing-mode: vertical-rl;">
                    {filetered_data.get("bottom").get("x")[i].substring(0,8) + " -"}</text>
                <text x="{l_bottom_scale_x(i+0.8)}%" y="{bottom_scale_y(-0.02)}%" style="writing-mode: vertical-rl;">
                    {filetered_data.get("bottom").get("x")[i].split("-")[1].substring(0,9)}</text>
            {/each}

            {#each [0.2,0.4,0.6,0.8,1] as i}
                <line class="tick" y1="{bottom_scale_y(i)}%" y2="{bottom_scale_y(i)}%" x1="{bottom_scale_x(-0.15)}%" x2="{bottom_scale_x(0.15)}%" />
                <text x="{bottom_scale_x(-1.3)}%" y="{bottom_scale_y(i)+1.3}%" style="font-size: 13px;">{((i*filetered_data.get("bottom").get("max"))+"").split(".")[0]}</text>
            {/each}
        </svg>
    </div><!-- end botL -->
    <div class="item6"><!-- botR -->
        <div class="heading">
            Attendancies per sports type (averaged per game)
        </div>
        <svg class="bottpic" style="">
            <line class="axis" id="x" x1="{bottom_scale_x(-0.5)}%" y1="{bottom_scale_y(0)}%" x2="{bottom_scale_x(bot_num_x_ticks+0.5)}%" y2="{bottom_scale_y(0)}%" />
            <line class="axis" id="y" x1="{bottom_scale_x(0)}%" y1="{bottom_scale_y(-0.04)}%" x2="{bottom_scale_x(0)}%" y2="{bottom_scale_y(1.025)}%" />

            {#each bot_ticks as i}
                <line class="tick" y1="{bottom_scale_y(-0.02)}%" y2="{bottom_scale_y(0.02)}%" x1="{bottom_scale_x(i+1)}%" x2="{bottom_scale_x(i+1)}%" />

                {#each [1,2,3,4,5,6,7,8] as group}
                    {#if group == 1}
                        <line class="bar" style="stroke: {bot_color[group-1]};" y1="{bottom_scale_y(0)}%" y2="{bottom_scale_y(filetered_data.get("bottom").get(group+"")[i])}%" 
                        x1="{bottom_scale_x(i+1)}%" x2="{bottom_scale_x(i+1)}%" />
                    {:else}
                        <line class="bar" style="stroke: {bot_color[group-1]};" y1="{bottom_scale_y(filetered_data.get("bottom").get((group-1)+"")[i])}%" 
                        y2="{bottom_scale_y(filetered_data.get("bottom").get(group+"")[i])}%" x1="{bottom_scale_x(i+1)}%" x2="{bottom_scale_x(i+1)}%" />
                    {/if}
                {/each}

                <text x="{bottom_scale_x(i+1.2)}%" y="{bottom_scale_y(-0.02)}%" style="writing-mode: vertical-rl;">
                    {filetered_data.get("bottom").get("x")[i].substring(0,8) + " -"}</text>
                <text x="{bottom_scale_x(i+0.8)}%" y="{bottom_scale_y(-0.02)}%" style="writing-mode: vertical-rl;">
                    {filetered_data.get("bottom").get("x")[i].split("-")[1].substring(0,9)}</text>
            {/each}

            {#each [1,2,3,4,5,6,7,8] as group}<!-- labels right to plot -->
                <line style="stroke: {bot_color[group-1]}; stroke-width: 3%" y1="{bottom_scale_y(1 - ((9-group) * 0.1))}%" y2="{bottom_scale_y(1 - ((9-group) * 0.1)) - 4}%"
                x1="{bottom_scale_x(bot_num_x_ticks+1)}%" x2="{bottom_scale_x(bot_num_x_ticks+1)}%" />
                <text x="{bottom_scale_x(bot_num_x_ticks+1.5)}%" y="{bottom_scale_y(1 - ((9-group) * 0.1))}%">{sports_types.get(group+"")}</text>
            {/each}

            {#each [0.2,0.4,0.6,0.8,1] as i}
                <line class="tick" y1="{bottom_scale_y(i)}%" y2="{bottom_scale_y(i)}%" x1="{bottom_scale_x(-0.15)}%" x2="{bottom_scale_x(0.15)}%" />
                <text x="{bottom_scale_x(-1.2)}%" y="{bottom_scale_y(i)+1.3}%" style="font-size: 13px;">{i*100}%</text>
            {/each}
        </svg>
    </div><!-- end botR -->
</div>

<!-- class .   id # -->
<style>
    .sidebar {
        border-width: 1px; 
        border-radius: 5px; 
        border-color: grey; 
        border-style: solid; 
        width: 98%; 
        margin-left: 1%;
        padding: 1%;
    }
    .left_stats {
        border-width: 2px; 
        border-radius: 3px; 
        border-color: grey; 
        border-style: solid; 
        width: 98%; 
        margin: 1%;
        padding: 1%;
        text-align: center;

    }
    .bottpic {
        width:99%; 
        height: 90%; 
        margin: 5px;
        padding: 3px;
        border: 1px gray solid;
        border-radius: 13px;
        font-size: 16px; 
        font-weight: normal;
    }
    .item5 .bar {
        stroke-width: 3%;
    }
    .item6 .bar {
        stroke-width: 4%;
    }
    .tick{
        stroke: black;
        stroke-width: 2;

    }
    .axis{
        stroke: black;
        stroke-width: 2;
    }
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
    .item3 { grid-area: topM; }
    .item4 { grid-area: topR; }
    .item5 { 
        grid-area: botL;
        font-size: 20px; 
        font-weight: bold;
        padding: 3px;
    }
    .item6 { 
        grid-area: botR;
        font-size: 20px; 
        font-weight: bold;
        padding: 3px;
    }
    .grid-container {
        display: grid;
        grid-template-areas:
            'left topL topL topM topM topR topR'
            'left topL topL topM topM topR topR'
            'left botL botL botL botR botR botR'
            'left botL botL botL botR botR botR';
        gap: 14px;
        /*background-color: #77797a;*/
        padding: 2px;
        grid-template-columns: repeat(7, 1fr);
        grid-template-rows: repeat(4, 1fr);
    }
    .grid-container>*{
        border-radius: 7px;
        background-color: white;
        box-shadow: 0px 0px 10px #a1a1a1;
    }

    .item2 { 
        grid-area: topL;
        /* display: flex;
        flex-direction: row;
        justify-content: space-between;
        overflow-y: auto; */
    }
    .top_pic {
        width:49%; 
        height: 90%;
        border: 1px;
        /* border-style: solid;
        border-color: gray; */
        font-size: 16px; 
        font-weight: normal;
        text-align: center;
        flex-direction: row;
        float: left;
        position:relative;
    }
    .mid_pic {
        width:33%; 
        height: 100%;
        /* border: 1px;
        border-style: solid;
        border-color: gray; */
        font-size: 16px; 
        font-weight: normal;
        text-align: center;
        flex-direction: row;
        float: left;
        position:relative;
    }
    .top_m_outer {
        height: 30%; 
        width: 100%; 
        padding: 1px; 
        font-size: 20px; 
        font-weight: bold;
    }
    .top_m_sports {
        font-weight: bold; 
        margin-top: 3%;
    }

    .top_r_box {
        text-align: left;
        height: 1.5em;
        vertical-align: middle;
        position: absolute; 
        left: 5%;
        margin-left: 7%;
    }
    .top_r_text {
        position: absolute;
        left: 10%;
        top: 7%;
    }
    .top_r_outer {
        height: 49%; 
        width: 100%; 
        padding: 3px; 
        font-size: 20px; 
        font-weight: bold;
    }
    .medals {
        width: 8%;
        margin-right: 5%;
    }

    .podium {
        position: absolute;
        bottom: 0.7em;
        left: 0.45em;
    }

    .podium2 {
        position: absolute;
        top: 2em;
        left: 0.45em;
    }

    .heading {
        font-size: 20px;
        text-align: center;
        font-weight: bold;
    }
    .text_l {
        font-size: 18px;
        font-weight: bold;
    }


    :global(body) {
        background-color: rgb(233, 233, 233);
        font-family: sans-serif;
    }
    .grid-container > div {/* div elements of the grid */
        background-color: rgb(233, 233, 233);
    }

    .show {
        border: 1px;
        border-style: solid;
        border-color: greenyellow;
    }

    .tooltipped{
        position: relative;
    }

    .tooltipped .tooltip{
        position: absolute;
        visibility: hidden;
        opacity: 0;
        z-index: 1;
        background-color: #00000038;
        color: white;
        border-radius: 7px;
        padding: 7px;
        backdrop-filter: blur(10px);
        transition: all 0.25s;
        font-weight: 300;
    }
    .tooltipped .tooltip.tooltip-right{
        /*top: 0;
        left: 100%;
        min-height: 100%;*/
        top: 100%;
        left: 30%;
        width: 70%;
        border-top-left-radius: 0;
    }
    .tooltipped .tooltip.tooltip-bottom{
        top: 100%;
        left: 0;
        min-width: 100%;
    }
    .tooltipped:hover .tooltip{
        opacity: 1;
        visibility: visible;
    }
    .list_tool {
        margin: 0px;
        padding: 0 0 0 16px;
        
    }
    .list_tool > li {
        /*margin-left: -15%;
        margin-top: -12%;
        margin-bottom: 0%;*/
        margin: 0;
        padding: 0;
        line-height: 1em;
    }

    label{
        display:inline-block;
        word-wrap: break-word;
    }
    .uistack{
        display: flex;
        width: 100%;
        box-sizing: border-box;
        gap: 7px;
    }
    .uistack input{
        align-self: flex-start;

    }
    .uistack label{
        flex-grow: 1;
    }
</style>

