<script>
	import { _tick, user } from '$lib/store.js';

	import Card from '$lib/card.svelte';
	import Item from '$lib/item/index.svelte';
	import Photo from './photo.svelte';
	import Info from './info.svelte';
	import Desc from './desc.svelte';
	import Feedback from './feedback.svelte';
	import Meta from '$lib/meta.svelte';
	import Floater from './floater.svelte';

	import Button from '$lib/button.svelte';

	export let data;
	let { item } = data;
	let { recently_viewed } = data;

	$: if ($_tick) {
		item = $_tick;
		$_tick = '';
	}

	let edit_mode = true;
</script>

<Meta title={item.name} description={item.desc} image={item.thumbnail} />

<Card>
	<div class="title">
		Item Details
		{#if $user && $user.roles.includes('admin')}
			<Button
				name="Edit Mode: {edit_mode ? 'On' : 'Off'}"
				class="tiny"
				icon="edit"
				icon_size="12"
				on:click={() => {
					edit_mode = !edit_mode;
				}}
			/>
		{/if}
	</div>

	<section class="block">
		<div class="photo">
			<Photo {item} />
		</div>

		<div>
			<Info {item} />
			<Desc {item} />
			<Feedback {item} />
			<Floater {item} />
		</div>
	</section>
</Card>

{#if recently_viewed && recently_viewed.length > 0}
	<Card>
		<div class="title">Recently Viewed</div>
		<div class="items" class:grid={true}>
			{#each recently_viewed as item (item.key)}
				<Item {item} />
			{/each}
		</div>
	</Card>
{/if}

<style>
	.block {
		display: flex;
		flex-direction: column;
		gap: var(--sp2);
	}
	.block > div {
		width: 100%;
	}

	@media screen and (min-width: 800px) {
		.block {
			flex-direction: unset;
			position: relative;
			
			margin-top: var(--sp2);
		}

		.photo {
			position: sticky;
			top: var(--sp2);

			align-self: flex-start;
		}
	}

	.title {
		font-weight: 600;
		display: flex;
		justify-content: space-between;
	}

	.items {
		display: grid;
		gap: var(--sp2);
		grid-template-columns: 1fr;

		margin-top: var(--sp4);
		color: var(--ac1);
	}
	.grid {
		grid-template-columns: repeat(2, 1fr);
	}
	@media screen and (min-width: 700px) {
		.grid {
			grid-template-columns: repeat(3, 1fr);
		}
	}
	@media screen and (min-width: 1000px) {
		.grid {
			grid-template-columns: repeat(4, 1fr);
		}
	}
</style>
