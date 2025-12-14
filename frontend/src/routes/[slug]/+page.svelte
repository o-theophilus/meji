<script>
	import { page } from '$app/state';
	import { onMount } from 'svelte';
	import { module, app } from '$lib/store.svelte.js';

	import { Content } from '$lib/layout';
	import { Button, Toggle } from '$lib/button';
	import { Meta, Log } from '$lib/macro';
	import Edit_Button from './edit_button.svelte';

	import { Status, Photo, Name, Tags, Price, Information, Quantity, Feedback, Variation } from '.';
	import Highlight from './highlight.svelte';
	import Similar from './similar.svelte';
	import ToTop from './to_top.svelte';

	import Like from '../shop/like.svelte';
	import Share from './share.svelte';
	import AddCart from './add_to_cart.svelte';

	let { data } = $props();
	let item = $derived(data.item);
	let edit_mode = $state(false);
	let is_admin = $state(false);

	const update = (data) => {
		item = data;
	};

	let comment = $state();
	let similar = $state();

	const refresh = async (data) => {
		item = data;

		edit_mode = false;
		await comment.load();
		await similar.load();
	};

	onMount(async () => {
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/admin/access/item:edit`);
		resp = await resp.json();
		if (resp.status == 200) {
			is_admin = app.user.access.some((x) => resp.access.includes(x));
		}

		if (page.url.searchParams.has('edit') && is_admin) {
			page.url.searchParams.delete('edit');
			edit_mode = true;
			window.history.replaceState(history.state, '', page.url.href);
		}

		refresh(item);
	});

	let edata = $state({
		comment: 0,
		like: 0,
		dislike: 0,
		share: 0,
		view: 0,
		user_like: null
	});
</script>

{#key item.key}
	<Log action={'viewed'} entity_key={item.key} entity_type={'item'} />
{/key}
<Meta title={item.name} description={item.description} image={item.photo} />

<Content>
	{#if is_admin}
		<Toggle state_2="edit" active={edit_mode} onclick={() => (edit_mode = !edit_mode)} />
		<br />
	{/if}

	{#if edit_mode && (app.user.access.includes('item:edit_status') || app.user.access.includes('item:edit_highlight'))}
		<div class="line status">
			<Status {item} {update}></Status>
			<Highlight {item} />
		</div>
	{/if}

	<div class="photo_info">
		<div class="photo">
			<Photo bind:item {edit_mode} {update} />
		</div>

		<div class="info">
			<Name {item} {edit_mode} {update} />
			<Tags {item} {edit_mode} {update} />
			<Price {item} {edit_mode} {update} />
			<Information {item} {edit_mode} {update} />
			<Variation {item} {edit_mode} {update} />
			<Quantity {item} {edit_mode} {update} />
			<Feedback {item} bind:this={comment} />
		</div>
	</div>
</Content>

<div class="floater">
	<div class="floater_block">
		<Button icon="cart" onclick={() => module.open(AddCart, item)}>Add to Chat</Button>
		<Button
			icon="whatsapp"
			href="https://api.whatsapp.com/send?phone=+2349113717298&text=Hi%0AI want to make enquiry concerning ${item.name} on Meji.ng%20{page
				.url.href}"
			target="_blank"
		>
			Chat
		</Button>

		<Like {item} />

		<Button icon="share-2" onclick={() => module.open(Share, item)}></Button>
	</div>
</div>

<Content --content-height --content-padding-top="0" --content-padding-bottom="0">
	<Similar key={item.key} bind:this={similar} {refresh} />
	<ToTop />
</Content>

<style>
	.photo_info {
		display: flex;
		flex-direction: column;
		gap: var(--sp3);
	}
	.info {
		margin-top: var(--sp3);
	}

	.photo,
	.info {
		width: 100%;
	}

	.floater {
		position: sticky;
		bottom: var(--headerHeight);

		background-color: var(--bg1);
		border-top: 1px solid var(--bg2);
	}

	.floater_block {
		padding: 8px 24px;
		max-width: var(--mobileWidth);
		margin: auto;
	}

	@media screen and (min-width: 800px) {
		.photo_info {
			flex-direction: unset;
			position: relative;
		}

		.photo {
			position: sticky;
			top: var(--sp2);

			align-self: flex-start;
		}

		.info {
			margin: 0;
		}
	}

	.line.status {
		margin-bottom: 8px;
	}
</style>
