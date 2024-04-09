<script>
	import { slide } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';
	import { loading, toast } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Center from '$lib/center.svelte';
	import Card from '$lib/card.svelte';
	import Meta from '$lib/meta.svelte';
	import ButtonFold from '$lib/button.fold.svelte';
	import Button from '$lib/button.svelte';
	import Back from '$lib/button.back.svelte';

	export let data;
	let { unused } = data;
	let { users } = data;
	let { items } = data;
	let { adverts } = data;

	let open_unused = unused.length > 0;
	let open_users = users.length > 0;
	let open_items = items.length > 0;
	let open_adverts = adverts.length > 0;

	let photos = [];
	let error = {};

	const remove = async () => {
		error = {};

		$loading = 'deleting . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/photo/error`, {
			method: 'delete',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({ photos })
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			unused = unused.filter((x) => !photos.includes(x));
			$toast = {
				status: 200,
				message: `Photo${photos.length > 1 ? 's' : ''} Deleted`
			};
			photos = [];
		} else {
			error = resp;
		}
	};
</script>

<Meta title="Manage Photos" description="Here you will find missing or excess images" />

<Center>
	<br />
	<div class="ctitle">
		<div class="ctitle">
			<Back />
			Photo Error
		</div>
	</div>
</Center>

<Card>
	<div class="title">
		Unused Photos ({unused.length})
		<ButtonFold
			open={open_unused}
			on:click={() => {
				open_unused = !open_unused;
			}}
		/>
	</div>

	{#if open_unused}
		<br />
		<div class="unused" transition:slide|local={{ delay: 0, duration: 200, easing: cubicInOut }}>
			{#each unused as x}
				<img
					class:selected={photos.includes(x)}
					src={`${x}/100` || '/image/item.png'}
					alt="missing"
					onerror="this.src='/image/item.png'"
					on:click={() => {
						if (photos.includes(x)) {
							photos = photos.filter((y) => y != x);
						} else {
							photos.push(x);
							photos = photos;
						}
					}}
					role="presentation"
				/>
			{:else}
				no item here
			{/each}
		</div>

		<br />
		{#if error.error}
			<span class="error">
				{error.error}
			</span>
			<br />
			<br />
		{/if}

		{#if unused.length > 0}
			<div class="line">
				<Button
					on:click={() => {
						if (photos.length != unused.length) {
							photos = [];
							photos = unused;
						} else {
							photos = [];
						}
					}}
				>
					Select
				</Button>
				<Button class="hover_red" on:click={remove} disabled={photos.length == 0}>Delete</Button>
			</div>
		{/if}
	{/if}
</Card>

<Card>
	<div class="title">
		Users ({users.length})
		<ButtonFold
			open={open_users}
			on:click={() => {
				open_users = !open_users;
			}}
		/>
	</div>

	{#if open_users}
		<br />
		<div transition:slide|local={{ delay: 0, duration: 200, easing: cubicInOut }}>
			{#each users as x}
				<a href="/profile?user={x.key}">{x.name}</a>

				<br />
			{:else}
				no item here
			{/each}
		</div>
	{/if}
</Card>

<Card>
	<div class="title">
		Items ({items.length})
		<ButtonFold
			open={open_items}
			on:click={() => {
				open_items = !open_items;
			}}
		/>
	</div>

	{#if open_items}
		<br />
		<div transition:slide|local={{ delay: 0, duration: 200, easing: cubicInOut }}>
			{#each items as x}
				<a href="/{x.key}">{x.name}</a>

				<br />
			{:else}
				no item here
			{/each}
		</div>
	{/if}
</Card>

<Card>
	<div class="title">
		Adverts ({adverts.length})
		<ButtonFold
			open={open_adverts}
			on:click={() => {
				open_adverts = !open_adverts;
			}}
		/>
	</div>

	{#if open_adverts}
		<br />
		<div transition:slide|local={{ delay: 0, duration: 200, easing: cubicInOut }}>
			{#each adverts as x}
				<a href="/admin/adverts/{x.key}">{x.name}</a>

				<br />
			{:else}
				no item here
			{/each}
		</div>
	{/if}
</Card>

<style>
	.title {
		font-weight: 900;
		display: flex;
		justify-content: space-between;
		align-items: center;
	}

	.line {
		display: flex;
		gap: var(--sp0);
	}

	.unused {
		line-height: 0;
		display: flex;
		flex-wrap: wrap;
		gap: var(--sp1);
	}
	img {
		border-radius: var(--sp0);
		cursor: pointer;
	}
	img.selected {
		outline: 2px solid var(--cl1);
	}
</style>
