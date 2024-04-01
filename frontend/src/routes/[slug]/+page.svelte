<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { user, loading, portal } from '$lib/store.js';

	import Card from '$lib/card.svelte';
	import Meta from '$lib/meta.svelte';
	import Log from '$lib/log.svelte';
	import Button from '$lib/button.svelte';
	import Group from '$lib/group.svelte';
	import ButtonFold from '$lib/button.fold.svelte';
	import Photo from './photo.svelte';
	import Info from './info.svelte';
	import SVG from '$lib/svg.svelte';
	import Center from '$lib/center.svelte';

	export let data;
	$: recently_viewed = data.recently_viewed;
	$: similar_items = data.similar_items;
	$: customer_view = data.customer_view;
	$: item = data.item;

	$: if ($portal) {
		if ($portal.type == 'item') {
			item = $portal.data;
		}
		$portal = '';
	}

	let edit_mode = false;
	$loading = false;

	let permissions = [
		'item:edit_photo',
		'item:advert',
		'item:edit_status',
		'item:edit_name',
		'item:edit_tag',
		'item:edit_price',
		'item:edit_info',
		'item:edit_variation'
	];
	let is_admin = $user.permissions.some((x) => permissions.includes(x));

	onMount(() => {
		if ($page.url.searchParams.has('edit') && is_admin) {
			$page.url.searchParams.delete('edit');
			edit_mode = true;

			window.history.replaceState(history.state, '', $page.url.href);
		}
	});
</script>

<Meta title={item?.name} description={item.info} image="{item.photos[0]}/200" />
{#key item.key}
	<Log action={'viewed'} entity_key={item.key} entity_type={'item'} />
{/key}

<Center>
	<br />
	<div class="ctitle">
		Item Details
		{#if $user && is_admin}
			<Button
				class="outline"
				on:click={() => {
					edit_mode = !edit_mode;
				}}
			>
				<SVG type="edit" size="10" />
				Edit: {edit_mode ? 'On' : 'Off'}
			</Button>
		{/if}
	</div>
</Center>

<Card>
	<section class="block">
		<div class="photo">
			<Photo {item} edit_mode={edit_mode && $user.permissions.includes('item:edit_photo')} />
		</div>

		<div>
			{#if edit_mode && $user.permissions.includes('item:advert')}
				<Button class="link" href="/admin/adverts/{item.key}">Advert &gt;</Button>
				<br />
				<br />
			{/if}
			<Info {item} {edit_mode} />
		</div>
	</section>
</Card>

<Group let:open let:set_open name="Recently Viewed" items={recently_viewed}>
	<ButtonFold {open} on:click={set_open} />
</Group>
<Group let:open let:set_open name="Similar Items" items={similar_items}>
	<ButtonFold {open} on:click={set_open} />
</Group>
<Group let:open let:set_open name="Customers who viewed this also viewed" items={customer_view}>
	<ButtonFold {open} on:click={set_open} />
</Group>

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

		.photo {
			position: sticky;
			top: var(--sp2);

			align-self: flex-start;
		}
	}
</style>
