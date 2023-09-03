<script>
	import { slide } from 'svelte/transition';
	import { elasticInOut } from 'svelte/easing';
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { user, loading, portal } from '$lib/store.js';

	import Card from '$lib/card.svelte';
	import Item from '$lib/item/index.svelte';
	import Meta from '$lib/meta.svelte';
	import Button from '$lib/button.svelte';
	import Button_Fold from '$lib/button_fold.svelte';
	import Photo from './photo.svelte';
	import Info from './info.svelte';

	export let data;
	$: item = data.item;
	$: recently_viewed = data.recently_viewed;

	$: if ($portal) {
		item = $portal;
		$portal = '';
	}

	let edit_mode = false;
	let open_recent = true;
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
			<Photo {item} {edit_mode} />
		</div>
		<div>
			<Info {item} {edit_mode} />
		</div>
	</section>
</Card>

{#if recently_viewed && recently_viewed.length > 0}
	<Card>
		<div class="title">
			Recently Viewed
			{#if $user && $user.roles.includes('admin')}
				<Button_Fold
					open={open_recent}
					on:click={() => {
						open_recent = !open_recent;
					}}
				/>
			{/if}
		</div>

		{#if open_recent}
			<div
				class="item_area"
				class:list={$user.setting.item_view == 'list'}
				transition:slide|local={{ delay: 0, duration: 200, easing: elasticInOut }}
			>
				{#each recently_viewed as item (item.key)}
					<Item {item} />
				{/each}
			</div>
		{/if}
	</Card>
{/if}

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
