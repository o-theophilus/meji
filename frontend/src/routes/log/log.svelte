<script>
	import { user } from '$lib/store.js';
	import { createEventDispatcher } from 'svelte';

	let emit = createEventDispatcher();
	export let log;

	let href = '';
	if (['item', 'cart'].includes(log.entity_type)) {
		href = `/${log.entity_key}`;
	} else if (log.entity_type == 'order') {
		href = `/orders/${log.entity_key}`;
	} else if (log.entity_type == 'voucher') {
		href = `/admin/vouchers/${log.entity_key}`;
	} else if (log.entity_type == 'advert') {
		href = `/admin/adverts/${log.entity_key}`;
	}
</script>

<section>
	<div
		class="status"
		class:good={log.status == 200}
		class:caution={![200, 400].includes(log.status)}
		class:error={log.status == 400}
	/>
	<span class="date">
		{log.date.split('T').join(' ')}
	</span>
	<br />

	<!-- TODO: FOR DELETED USERS -->
	{#if log.user_name}
		<a data-sveltekit-preload-data="off" href="/profile?search={log.user_key}">
			{log.user_name}
		</a>
	{:else}
		<span class="bold"> Deleted User </span>
	{/if}

	{#if log.user_key && $user.roles.includes('log:view')}
		<button
			on:click={() => {
				emit('search', { user: log.user_key });
			}}
		>
			&#9679;
		</button>
	{/if}

	{log.action}

	{#if !['auth', 'user'].includes(log.entity_type)}
		{log.entity_type}
	{/if}

	{#if !['auth', 'user', 'otp'].includes(log.entity_type)}
		<a data-sveltekit-preload-data="off" {href}>
			{log.entity_name}
		</a>

		<button
			on:click={() => {
				emit('search', { entity: log.entity_key });
			}}
		>
			&#9679;
		</button>
	{/if}

	{#if log.misc}
		<br />
		{#each Object.entries(log.misc) as [key, value], i}
			{#if i != 0},{/if}
			{key}: {value}
		{/each}
	{/if}
</section>

<style>
	section {
		padding: var(--sp2) 0;
		border-bottom: 2px solid var(--ac5);
	}

	.status {
		display: inline-block;
		--size: 10px;
		width: var(--size);
		height: var(--size);

		border-radius: 50%;

		background-color: var(--cl5);
		color: var(--ac6_);
	}
	.good {
		background-color: var(--cl5);
	}
	.caution {
		background-color: var(--cl3);
	}
	.error {
		background-color: var(--cl4);
	}

	.bold {
		font-weight: 500;
	}

	.date {
		font-size: smaller;
		color: var(--ac3);
	}

	a {
		color: var(--cl1);
		text-decoration: none;
		font-weight: 500;
	}
	button {
		color: var(--cl1);
		border: none;
		background-color: transparent;
		cursor: pointer;
	}

	button:hover,
	a:hover {
		color: var(--cl2);
	}
</style>
