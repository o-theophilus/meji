<script>
	import { onMount } from 'svelte';
	
	import Ads from './ads_block.svelte';

	let ads = [];

	onMount(async () => {
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/ads`);
		resp = await resp.json();

		if (resp.status == 200) {
			ads = resp.ads;
		}
	});
</script>

<div class="x300x300">
	<Ads {ads} size="300x300" />
</div>
<div class="x600x300">
	<Ads {ads} size="600x300" />
</div>
<div class="x900x300">
	<Ads {ads} size="900x300" />
</div>

<style>
	.x900x300,
	.x600x300 {
		display: none;
	}

	@media screen and (min-width: 700px) {
		.x300x300,
		.x900x300 {
			display: none;
		}
		.x600x300 {
			display: unset;
		}
	}
	@media screen and (min-width: 1000px) {
		.x300x300,
		.x600x300 {
			display: none;
		}
		.x900x300 {
			display: unset;
		}
	}
</style>
