<script>
	import { portal } from '$lib/store.js';

	import Card from '$lib/card.svelte';
	import Meta from '$lib/meta.svelte';
	import Center from '$lib/center.svelte';
	import Button from '$lib/button.svelte';
	import Back from '$lib/button.back.svelte';
	import Advert from './advert.svelte';
	import Placement from './place.svelte';

	export let data;
	let { advert } = data;
	let { item } = data;
	let { ad_space } = data;

	$: if ($portal) {
		if ($portal.type == 'advert') {
			advert = $portal.data;
		}
		$portal = '';
	}
</script>

<Meta title={item.name} description={item.name} image={item.photos[0]} />

<Center>
	<br />
	<div class="ctitle">
		<div class="ctitle">
			<Back />
			<Button class="link" href="/{item.slug}">
				{item.name}
			</Button>
			- Adverts
		</div>
	</div>
</Center>

<Card>
	<section class="block">
		<div>
			<Advert {item} {advert} />
		</div>

		<div>
			<Placement {advert} {ad_space} />
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
