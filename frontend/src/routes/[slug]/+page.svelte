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
	import SVG from '$lib/svg.svelte';
	import Center from '$lib/center.svelte';

	import Status from './status.svelte';
	import Name from './name.svelte';
	import Tag from './tag.svelte';
	import Price from './price.svelte';
	import Info from './info.svelte';
	import Variation from './variation.svelte';
	import Feedback from './feedback.svelte';
	import Floater from './floater.svelte';

	export let data;
	$: item = data.item;
	$: feedbacks = data.feedbacks;
	$: give_feedback = data.give_feedback;
	$: groups = data.groups;

	onMount(() => {
		if ($page.url.searchParams.has('edit') && is_admin) {
			$page.url.searchParams.delete('edit');
			edit_mode = true;

			window.history.replaceState(history.state, '', $page.url.href);
		}
	});

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
	let edit_mode = false;
	$loading = false;

	let all_tags = {
		loaded: false,
		data: []
	};
	$: if ($portal) {
		if ($portal.type == 'item') {
			item = $portal.data;
		} else if ($portal.type == 'tag') {
			all_tags = $portal.data;
		}
		$portal = '';
	}
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

			<Status {item} {edit_mode} />
			<Name {item} {edit_mode} />
			{#key item.key}
				<Tag {item} {edit_mode} {all_tags} />
			{/key}
			<br />
			<Price {item} {edit_mode} />
			<br />
			<Info {item} {edit_mode} />
			<br />
			<Variation {item} {edit_mode} />
			<br />
			<Feedback {item} {feedbacks} {give_feedback} />
			<Floater {item} />
		</div>
	</section>
</Card>

{#each groups as x}
	<Group open={x.open} let:open let:set_open name={x.name} items={x.items}>
		<ButtonFold {open} on:click={set_open} />
	</Group>
{/each}

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
