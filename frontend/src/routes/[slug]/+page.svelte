<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { user, loading, portal } from '$lib/store.js';
	import { invalidate } from '$app/navigation';

	import Card from '$lib/card.svelte';
	import Meta from '$lib/meta.svelte';
	import Log from '$lib/log.svelte';
	import Button from '$lib/button.svelte';
	import Toggle from '$lib/button.toggle.svelte';
	import Group from '$lib/group.svelte';
	import ButtonFold from '$lib/button.fold.svelte';
	import Photo from './photo.svelte';
	import Center from '$lib/center.svelte';

	import Status from './status.svelte';
	import Name from './name.svelte';
	import Tag from './tag.svelte';
	import Price from './price.svelte';
	import Info from './info.svelte';
	import Variation from './variation.svelte';
	import Feedback from './feedback.svelte';
	import Floater from './floater.svelte';
	import Spinner from '$lib/loading_spinner.svelte';
	import Refresh from './refresh.svelte';

	export let data;
	$: status = data.status;
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
		if (status == 202) {
			invalidate(() => true);
		}
	};
</script>

<Meta title={item?.name} description={item.info} image="{item.photos[0]}/200" />
{#key item.key}
	<Log action={'viewed'} entity_key={item.key} entity_type={'item'} />
	<Refresh on:refresh={refresh} />
{/key}

<Center>
	<br />
	<div class="ctitle">
		Item Details
		{#if $user && is_admin}
			<Toggle
				active={edit_mode}
				state_2="edit"
				on:click={() => {
					edit_mode = !edit_mode;
				}}
			/>
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
			<Tag {item} {edit_mode} />
			<br />
			<Price {item} {edit_mode} />
			<br />
			<Info {item} {edit_mode} />
			<br />
			<Variation {item} {edit_mode} />
			<br />
			<!-- {#key item.key} -->
			<!-- <Feedback {item} on:done={get_group} /> -->
			<!-- {/key} -->
			<Feedback {item} bind:get_feedback />
			<Floater {item} />
		</div>
	</section>
</Card>

{#each groups as x}
	<Group open={x.open} let:open let:set_open name={x.name} items={x.items}>
		<ButtonFold {open} on:click={set_open} />
	</Group>
{:else}
	<Card>
		<div class="skeleton_frame">
			{#each Array(10).slice(0, width < 700 ? 2 : width < 1000 ? 3 : 4) as _}
				<div class="item">
					<Spinner active size="20" />
				</div>
			{/each}
		</div>
	</Card>
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

	.skeleton_frame {
		display: grid;
		gap: var(--sp2);
		grid-template-columns: repeat(2, 1fr);

		color: var(--ac1);
	}

	@media screen and (min-width: 700px) {
		.skeleton_frame {
			grid-template-columns: repeat(3, 1fr);
		}
	}

	@media screen and (min-width: 1000px) {
		.skeleton_frame {
			grid-template-columns: repeat(4, 1fr);
		}
	}

	.skeleton_frame .item {
		display: flex;
		justify-content: center;
		align-items: center;
		aspect-ratio: 1/1;

		width: 100%;
		border-radius: var(--sp1);

		animation: blink 2s infinite linear;
	}

	@keyframes blink {
		0% {
			background-color: var(--ac5);
		}
		50% {
			background-color: var(--ac6);
		}
		100% {
			background-color: var(--ac5);
		}
	}
</style>
