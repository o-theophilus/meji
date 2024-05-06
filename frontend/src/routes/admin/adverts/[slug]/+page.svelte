<script>
	import { portal } from '$lib/store.js';

	import Card from '$lib/card.svelte';
	import Meta from '$lib/meta.svelte';
	import Center from '$lib/center.svelte';
	import Link from '$lib/button/link.svelte';
	import Back from '$lib/button/back.svelte';
	import Advert from './advert.svelte';
	import Space from './space.svelte';
	import Title from '$lib/title.svelte';

	export let data;
	let { advert } = data;
	let { item } = data;
	let { sizes } = data;
	let { spaces } = data;

	$: if ($portal) {
		if ($portal.type == 'advert') {
			advert = $portal.data;
		}
		$portal = '';
	}

	let photo_length = (a) => {
		let count = 0;
		for (let x of sizes) {
			if (a[`photo_${x}`]) {
				count++;
			}
		}
		return count;
	};
</script>

<Meta title="{item.name} Adverts" description="Manage images" />

<Center>
	<Title>
		<svelte:fragment slot="left">
			<Back />
		</svelte:fragment>
		Advert

		<svelte:fragment slot="down">
			<Link href="/{item.slug}" icon>
				{item.name}
			</Link>
		</svelte:fragment>
	</Title>
</Center>

<Card>
	<section class="block">
		<div>
			<Advert {item} {advert} {sizes} {photo_length} />
		</div>

		<div>
			<Space {advert} {spaces} {photo_length} />
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
