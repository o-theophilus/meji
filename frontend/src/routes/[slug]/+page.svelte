<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { user, loading, portal } from '$lib/store.js';

	import Card from '$lib/card.svelte';
	import Meta from '$lib/meta.svelte';
	import Button from '$lib/button.svelte';
	import Photo from './photo.svelte';
	import Info from './info.svelte';
	import SVG from '$lib/svg.svelte';

	import Group from './group.svelte';

	export let data;
	$: item = data.item;

	$: if ($portal) {
		item = $portal;
		$portal = '';
	}

	let edit_mode = false;
	$loading = false;

	onMount(() => {
		if ($page.url.searchParams.has('edit') && $user.roles.includes('admin')) {
			edit_mode = true;
			$page.url.searchParams.delete('edit');
			window.history.pushState(history.state, '', $page.url.href);
		}
	});
</script>

<Meta title={item?.name} description={item.info} image={item.thumbnail} />

<Card>
	<div class="title">
		Item Details
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
			<Photo {item} {edit_mode} />
		</div>
		<div>
			<Info {item} {edit_mode} />
		</div>
	</section>
</Card>

{#key item.key}
	<Group name="Recently Viewed" url="/recently_viewed/{$user.key}/{item.key}" />
	<Group name="Similar Items" url="/similar_items/{item.key}" />
	<Group name="Customers who viewed this also viewed" url="/customer_view/{$user.key}/{item.key}" />
{/key}

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
