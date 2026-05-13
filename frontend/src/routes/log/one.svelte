<script>
	import { Datetime } from '$lib/macro';
	import { app, page_state } from '$lib/store.svelte.js';
	import { slide } from 'svelte/transition';

	let { log, searchParams = $bindable() } = $props();
	let misc = $state(false);

	console.log(log);

	let href = $state('');
	if (log.entity.type == 'item') {
		href = `/${log.entity.key}`;
	} else if (log.entity.type == 'blog') {
		href = `/blog/${log.entity.key}`;
	} else if (log.entity.type == 'report') {
		href = `/admin/report?search=${log.entity.key}`;
	} else if (log.entity.type == 'page') {
		href = log.entity.key;
	} else if (log.entity.type == 'user') {
		href = `/@${log.entity.key}`;
	} else if (log.entity.type == 'comment') {
		href = `/${log.misc.post_key}#${log.entity.key}`;
	}

	// TODO: handle the href
	// added comment to blog
	// added comment to item
	// added item to cart
</script>

<section>
	<div
		class="status"
		class:_200={log.status == '200'}
		class:_201={!['200', '400'].includes(log.status)}
		class:_400={log.status == '400'}
	></div>

	<span class="date">
		<Datetime datetime={log.date_created} type="date_numeric" />
		<Datetime datetime={log.date_created} type="time_12h" />
	</span>
	<br />

	<a href="/@{log.user.username}" class="break">
		{log.user.name}
	</a>

	{#if log.user.key && app.user.access.includes('log.view_others')}
		<button
			class="misc"
			onclick={() => {
				searchParams.page_no = 1;
				searchParams.u_search = log.user.key;
				page_state.set({ u_search: log.user.key });
			}}
		>
			[search]
		</button>
	{/if}

	{log.action}
	<!-- {log.entity.type} -->

	{#if href}
		<a class="break" {href} data-sveltekit-preload-data="off">
			{log.entity.name}
		</a>

		<button
			class="misc"
			onclick={() => {
				searchParams.page_no = 1;
				searchParams.e_search = log.entity.key;
				page_state.set({ e_search: log.entity.key });
			}}
		>
			[search]
		</button>
	{/if}

	{#if Object.keys(log.misc).length}
		<button class="misc" onclick={() => (misc = !misc)}> [expand] </button>

		{#if misc}
			<div transition:slide>
				{#each Object.entries(log.misc) as [key, val]}
					<hr />
					{key}:
					<br />
					{#if log.entity.type == 'voucher' && key == 'validity'}
						<Datetime datetime={val} type="date" />
					{:else}
						<span class="break">
							{val}
						</span>
					{/if}
				{/each}
			</div>
		{/if}
	{/if}
</section>

<style>
	section {
		margin-top: 8px;
		color: var(--ft1);
		background-color: var(--bg3);
		border-radius: 8px;
		padding: 16px;
		outline: 1px solid var(--ol);
		outline-offset: -1pxs;

		font-size: 0.8rem;
	}

	.status {
		display: inline-block;
		--size: 10px;
		width: var(--size);
		height: var(--size);

		border-radius: 50%;
		color: var(--ac6_);
	}
	._200 {
		background-color: green;
	}
	._201 {
		background-color: var(--yellow);
	}
	._400 {
		background-color: red;
	}

	.date {
		font-size: 0.7rem;
		color: var(--ft2);
	}

	a {
		color: var(--cl1);
		text-decoration: none;
		font-weight: 700;
	}
	.misc {
		all: unset;
		cursor: pointer;

		color: var(--cl1);
		font-size: 0.7rem;
	}

	.misc:hover,
	a:hover {
		color: var(--cl1_b);
	}

	.break {
		word-wrap: break-word;
	}

	hr {
		margin: 8px 0;
	}
</style>
