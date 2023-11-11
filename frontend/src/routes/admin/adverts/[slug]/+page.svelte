<script>
	import { portal } from '$lib/store.js';

	import Card from '$lib/card.svelte';
	import Meta from '$lib/meta.svelte';
	import Center from '$lib/center.svelte';
	import Back from '$lib/button.back.svelte';
	import Advert from './advert.svelte';
	import Placement from './place.svelte';

	export let data;
	let advert = data.advert;
	let ad_space = data.ad_space;

	$: if ($portal) {
		if ($portal.type == 'advert') {
			advert = $portal.data;
		}
		$portal = '';
	}
</script>

<Meta title={advert.item.name} description={advert.item.name} image={advert.item.photo} />

<Center>
	<br />
	<div class="ctitle">
		<div class="ctitle">
			<Back />
			{advert.item.name} - Adverts
		</div>
	</div>
</Center>

<Card>
	<section class="block">
		<div>
			<Advert {advert} />
		</div>

		<div>
			<Placement {advert} {ad_space}/>
		</div>
	</section>
</Card>

<style>
	.block {
		display: flex;
		flex-direction: column;
		gap: var(--sp3);
	}
	.block > div {
		width: 100%;
	}

	@media screen and (min-width: 800px) {
		.block {
			flex-direction: unset;
			position: relative;
		}
	}
</style>
