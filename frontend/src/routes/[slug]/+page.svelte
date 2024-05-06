<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { user, loading, portal } from '$lib/store.js';

	import Card from '$lib/card.svelte';
	import Meta from '$lib/meta.svelte';
	import Log from '$lib/log.svelte';
	import Link from '$lib/button/link.svelte';
	import Toggle from '$lib/toggle.svelte';
	import Group from '$lib/item_group.svelte';
	import Photo from './photo.svelte';
	import Center from '$lib/center.svelte';
	import Title from '$lib/title.svelte';

	import Status from './status.svelte';
	import Name from './name.svelte';
	import Tag from './tag.svelte';
	import Price from './price.svelte';
	import Info from './info.svelte';
	import Variation from './variation.svelte';
	import Feedback from './feedback.svelte';
	import Floater from './floater.svelte';
	import Refresh from './refresh.svelte';
	import Skeleton from './item_group_skeleton.svelte';

	export let data;
	$: item = data.item;
	$: groups = data.groups;

	let edit_mode = false;
	let width;
	let is_admin = $user.permissions.some((x) =>
		[
			'item:edit_photo',
			'item:advert',
			'item:edit_status',
			'item:edit_name',
			'item:edit_tag',
			'item:edit_price',
			'item:edit_info',
			'item:edit_variation'
		].includes(x)
	);

	$: if ($portal) {
		if ($portal.type == 'item') {
			item = $portal.data;
		}
		$portal = '';
	}

	onMount(() => {
		if ($page.url.searchParams.has('edit') && is_admin) {
			$page.url.searchParams.delete('edit');
			edit_mode = true;

			window.history.replaceState(history.state, '', $page.url.href);
		}
		$loading = false;
	});

	let get_feedback;
	const refresh = async () => {
		await get_feedback();
	};
</script>

<Meta title={item?.name} description={item.info} image="{item.photos[0]}/200" />
{#key item.key}
	<Log action={'viewed'} entity_key={item.key} entity_type={'item'} />
	<Refresh on:refresh={refresh} />
{/key}

<Center>
	<Title>
		Item Details
		<svelte:fragment slot="right">
			{#if $user && is_admin}
				<Toggle
					active={edit_mode}
					state_2="edit"
					on:click={() => {
						edit_mode = !edit_mode;
					}}
				/>
			{/if}
		</svelte:fragment>
	</Title>
</Center>

<Card>
	<section class="block">
		<div class="photo">
			<Photo {item} edit_mode={edit_mode && $user.permissions.includes('item:edit_photo')} />
		</div>

		<div>
			{#if edit_mode && $user.permissions.includes('item:advert')}
				<Link href="/admin/adverts/{item.key}" icon>Advert</Link>
			{/if}

			<Status {item} {edit_mode} />
			<Name {item} {edit_mode} let:open>
				<Tag {item} {edit_mode} {open} />
			</Name>
			<Price {item} {edit_mode} />
			<Info {item} {edit_mode} />
			<Variation {item} {edit_mode} />
			{#key item.key}
				<Feedback {item} bind:get_feedback />
			{/key}
			<Floater {item} />
		</div>
	</section>
</Card>

{#each groups as x}
	<Group open={x.open} name={x.name} items={x.items} style={x.style} fold />
{:else}
	<Skeleton />
{/each}

<svelte:window bind:innerWidth={width} />

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
