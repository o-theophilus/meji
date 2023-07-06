<script>
	import { _tick } from '$lib/store.js';

	import Card from '$lib/comp/card.svelte';
	import Title from '$lib/comp/card_title.svelte';
	import Body from '$lib/comp/card_body_item.svelte';
	import Item from '$lib/item/index.svelte';
	import Photo from './photo.svelte';
	import Info from './info.svelte';
	import Desc from './desc.svelte';
	import Spec from './spec.svelte';
	import Feedback from './feedback.svelte';
	import Meta from '$lib/meta.svelte';
	import Floater from './floater.svelte';

	export let data;
	let { item } = data;
	let { recently_viewed } = data;

	$: if ($_tick) {
		item = $_tick;
		$_tick = '';
	}
</script>

<Meta title={item.name} description={item.desc} image={item.thumbnail} />

<section class="whole">
	<section class="details">
		<div class="block left">
			<Photo {item} />
		</div>
		<div class="block">
			<Card>
				<div class="block2">
					<Info {item} />
					<Desc {item} />
					<Spec {item} />
					<Feedback {item} />
					<Floater {item} />
				</div>
			</Card>
			<slot />
		</div>
	</section>

	{#if recently_viewed && recently_viewed.length > 0}
		<Card>
			<Title title="Recently Viewed" />
			<Body grid>
				{#each recently_viewed as item (item.key)}
					<Item {item} />
				{/each}
			</Body>
		</Card>
	{/if}
</section>

<style>
	.whole {
		display: grid;
		gap: var(--gap3);
	}
	.details {
		gap: var(--gap1);
		display: flex;
		flex-direction: column;
	}
	.block {
		display: flex;
		flex-direction: column;
		gap: var(--gap3);

		width: 100%;
	}

	@media screen and (min-width: 800px) {
		.details {
			flex-direction: unset;
			position: relative;
		}

		.left {
			position: sticky;
			top: var(--gap1);

			align-self: flex-start;
		}
	}
</style>
