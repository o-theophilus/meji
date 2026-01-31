<script>
	import { slide } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';
	import { flip } from 'svelte/animate';

	import { loading, notify, app } from '$lib/store.svelte.js';

	import { Content, Card } from '$lib/layout';
	import { FoldButton, Button, BackButton } from '$lib/button';
	import { Meta, Log, Icon } from '$lib/macro';
	import { Note, PageNote } from '$lib/info';

	let { data } = $props();
	let { users, items } = data;
	let unused_user_photo = $state(data.unused_user_photo);
	let unused_item_photo = $state(data.unused_item_photo);

	let open_unused_user = $derived(unused_user_photo.length > 0);
	let open_unused_item = $derived(unused_item_photo.length > 0);
	let open_users = $state(users.length > 0);
	let open_items = $state(items.length > 0);

	let selected_user_photo = $state([]);
	let selected_item_photo = $state([]);
	let error = $state({});

	const remove = async (photos, entity) => {
		error = {};

		loading.open(`Deleting ${entity} photo . . .`);
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/file_error`, {
			method: 'delete',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify({ photos, entity })
		});
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			notify.open(`${entity} photo${photos.length > 1 ? 's' : ''} deleted`);

			if (entity == 'user') {
				unused_user_photo = unused_user_photo.filter((x) => !photos.includes(x));
				selected_user_photo = [];
			} else if (entity == 'item') {
				unused_item_photo = unused_item_photo.filter((x) => !photos.includes(x));
				selected_item_photo = [];
			}
		} else {
			error = resp;
		}
	};
</script>

<Log entity_type={'page'} />
<Meta title="Manage / Excess Files"  />

<Content>
	<div class="line">
		<BackButton />
		<div class="page_title">Photo Error</div>
	</div>

	<br />

	<Card
		open={open_unused_user}
		onclick={() => {
			open_unused_user = !open_unused_user;
		}}
	>
		{#snippet title()}
			<div class="group_title">
				{unused_user_photo.length} Unused User Photo{unused_user_photo.length > 1 ? 's' : ''}
			</div>
		{/snippet}

		{#if unused_user_photo.length}
			<div class="photo_area">
				{#each unused_user_photo as x (x)}
					<img
						animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}
						class:selected={selected_user_photo.includes(x)}
						src={x.slice(-4) == '.jpg' ? `${x}/100` : '/no_preview.png'}
						loading="lazy"
						alt="unused file"
						onclick={() => {
							if (selected_user_photo.includes(x)) {
								selected_user_photo = selected_user_photo.filter((y) => y != x);
							} else {
								selected_user_photo.push(x);
								selected_user_photo = selected_user_photo;
							}
						}}
						onerror={(e) => (e.target.src = '/no_photo.png')}
						role="presentation"
					/>
				{/each}
			</div>
		{:else}
			<PageNote>
				<Icon icon="search" size="50" />
				<div class="none">No photo here</div>
			</PageNote>
		{/if}

		<Note status="400" note={error.user} --note-margin-top="16px"></Note>

		{#if unused_user_photo.length > 0}
			<div class="line btns">
				<Button
					onclick={() => {
						if (selected_user_photo.length != unused_user_photo.length) {
							selected_user_photo = [...unused_user_photo];
						} else {
							selected_user_photo = [];
						}
					}}
				>
					Select
					{#if selected_user_photo.length != unused_user_photo.length}
						All
					{:else}
						None
					{/if}
				</Button>
				<Button
					extra="hover_red"
					onclick={() => {
						remove(selected_user_photo, 'user');
					}}
					disabled={selected_user_photo.length == 0}
				>
					Delete ({selected_user_photo.length})
				</Button>
			</div>
		{/if}
	</Card>

	<Card
		open={open_unused_item}
		onclick={() => {
			open_unused_item = !open_unused_item;
		}}
	>
		{#snippet title()}
			<div class="group_title">
				{unused_item_photo.length} Unused item Photo{unused_item_photo.length > 1 ? 's' : ''}
			</div>
		{/snippet}

		{#if unused_item_photo.length}
			<div class="photo_area">
				{#each unused_item_photo as x (x)}
					<img
						animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}
						class:selected={selected_item_photo.includes(x)}
						src={x.slice(-4) == '.jpg' ? `${x}/100` : '/no_preview.png'}
						loading="lazy"
						alt="unused file"
						onclick={() => {
							if (selected_item_photo.includes(x)) {
								selected_item_photo = selected_item_photo.filter((y) => y != x);
							} else {
								selected_item_photo.push(x);
								selected_item_photo = selected_item_photo;
							}
						}}
						onerror={(e) => (e.target.src = '/no_photo.png')}
						role="presentation"
					/>
				{/each}
			</div>
		{:else}
			<PageNote>
				<Icon icon="search" size="50" />
				<div class="none">No photo here</div>
			</PageNote>
		{/if}

		<Note status="400" note={error.item} --note-margin-top="16px"></Note>

		{#if unused_item_photo.length > 0}
			<div class="line btns">
				<Button
					onclick={() => {
						if (selected_item_photo.length != unused_item_photo.length) {
							selected_item_photo = [...unused_item_photo];
						} else {
							selected_item_photo = [];
						}
					}}
				>
					Select
					{#if selected_item_photo.length != unused_item_photo.length}
						All
					{:else}
						None
					{/if}
				</Button>
				<Button
					extra="hover_red"
					onclick={() => {
						remove(selected_item_photo, 'item');
					}}
					disabled={selected_item_photo.length == 0}
				>
					Delete ({selected_item_photo.length})
				</Button>
			</div>
		{/if}
	</Card>

	<Card
		open={open_users}
		onclick={() => {
			open_users = !open_users;
		}}
	>
		{#snippet title()}
			<div class="group_title">
				{users.length} user{users.length > 1 ? 's' : ''} with missing photo
			</div>
		{/snippet}

		{#if users.length}
			<div class="link_area">
				{#each users as x}
					<a class="link" href="/@{x.username}">{x.name}</a>
				{/each}
			</div>
		{:else}
			<PageNote>
				<Icon icon="search" size="50" />
				<div class="none">No user here</div>
			</PageNote>
		{/if}
	</Card>

	<Card
		open={open_items}
		onclick={() => {
			open_items = !open_items;
		}}
	>
		{#snippet title()}
			<div class="group_title">
				{items.length} item{items.length > 1 ? 's' : ''} with missing photo
			</div>
		{/snippet}

		{#if items.length}
			<div class="link_area">
				{#each items as x}
					<a class="link" href="/{x.slug}">{x.name}</a>
				{/each}
			</div>
		{:else}
			<PageNote>
				<Icon icon="search" size="50" />
				<div class="none">No item here</div>
			</PageNote>
		{/if}
	</Card>
</Content>

<style>
	.group_title {
		font-weight: 800;
	}

	.photo_area {
		display: flex;
		flex-wrap: wrap;
		gap: 8px;
	}
	img {
		width: 100px;
		border-radius: 8px;
		cursor: pointer;
		background-color: var(--bg2);

		&.selected {
			outline: 2px solid var(--cl1);
		}
	}

	.btns {
		margin-top: 16px;
	}

	.link_area {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(80px, 1fr));
		gap: 4px;

		& .link {
			display: flex;
			align-items: center;

			padding: 4px;
			border-radius: 4px;

			line-height: 120%;
			color: var(--ft2);
			font-size: 0.7rem;
			text-decoration: none;
			background-color: var(--bg3);
			outline: 1px solid var(--ol);
			outline-offset: -1px;

			transition: background-color 0.2s ease-in-out;
			&:hover {
				background-color: var(--bg2);
				color: var(--ft1);
			}
		}
	}

	.none {
		font-size: 0.8rem;
	}
</style>
