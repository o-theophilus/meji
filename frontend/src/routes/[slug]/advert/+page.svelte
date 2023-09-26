<script>
	import { user, portal } from '$lib/store.js';

	import Card from '$lib/card.svelte';
	import Meta from '$lib/meta.svelte';
	import Button from '$lib/button.svelte';
	import Photo from './photo.svelte';
	import SVG from '$lib/svg.svelte';

	export let data;
	let { item } = data;
	let { advert } = data;

	$: if ($portal) {
		advert = $portal;
		$portal = '';
	}

	let edit_mode = false;
</script>

<Meta title="{item.name} ads" description="{item.name} ads" image={item.thumbnail} />

<Card>
	<div class="title">
		{item.name} Ads
		{#if $user && $user.roles.includes('admin')}
			<Button
				class="small"
				on:click={() => {
					edit_mode = !edit_mode;
				}}
			>
				<SVG type="edit" size="12" />
				Edit Mode: {edit_mode ? 'On' : 'Off'}
			</Button>
		{/if}
	</div>
	<section class="block">
		<div class="photo">
			<Photo {item} {advert} {edit_mode} />
		</div>
		<div>Controls</div>
	</section>
</Card>

<style>
	.block {
		display: flex;
		flex-direction: column;
		gap: var(--sp3);
		margin-top: var(--sp3);
	}
	.block > div {
		width: 100%;
	}

	@media screen and (min-width: 800px) {
		.block {
			flex-direction: unset;
			position: relative;
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
		align-items: center;
	}
</style>
