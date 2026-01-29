<script>
	import { slide } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';
	import { module } from '$lib/store.svelte.js';
	import { page } from '$app/state';

	import { Button, FoldButton, Toggle } from '$lib/button';
	import Confirm from './confirm.svelte';

	let user = module.value.user;
	let access = $state([...user.access]);
	let init = [...user.access];
	let active_name = $state('');
	let disabled = $derived(JSON.stringify([...access].sort()) == JSON.stringify([...init].sort()));

	const select = (x) => {
		access = access.includes(x) ? access.filter((p) => p !== x) : [...access, x];
	};
</script>

<section>
	<div class="page_title">Edit Access</div>

	{#each Object.entries(page.data.access) as [_type, level]}
		<div
			class="type"
			role="presentation"
			onclick={() => {
				if (active_name == _type) {
					active_name = '';
				} else {
					active_name = _type;
				}
			}}
		>
			{_type}
			<FoldButton open={active_name == _type} />
		</div>
		{#if active_name == _type}
			<div class="content" transition:slide|local={{ delay: 0, duration: 200, easing: cubicInOut }}>
				{#each Object.entries(level) as [lv, actions]}
					<div class="sub_type">
						Level {lv}
					</div>

					<div class="access_area">
						{#each actions as ac}
							<Toggle
								state_1=""
								state_2={ac.split('_').join(' ')}
								active={access.includes(`${_type}:${ac}`)}
								onclick={() => {
									select(`${_type}:${ac}`);
								}}
							/>
						{/each}
					</div>
				{/each}
			</div>
		{/if}
	{/each}

	<div class="line">
		<Button icon="history" onclick={() => (access = [...init])} {disabled}>Reset</Button>
		<Button
			icon2="send-horizontal"
			onclick={() =>
				module.open(Confirm, { access, user: module.value.user, update: module.value.update })}
			{disabled}>Submit</Button
		>
	</div>
</section>

<style>
	section {
		padding: var(--sp3);
	}

	.type {
		display: flex;
		align-items: center;
		gap: var(--sp2);
		justify-content: space-between;

		padding: var(--sp1) 0;
		cursor: pointer;
		text-transform: capitalize;
		font-weight: 900;
	}

	.content {
		border: 0 solid var(--bg1);
		border-width: 1px 0;
		padding-bottom: var(--sp1);
	}

	.sub_type {
		font-weight: 900;
		font-size: 0.8rem;
		margin: var(--sp1) 0;
	}

	.access_area {
		display: flex;
		align-items: center;
		gap: var(--sp0);
		flex-wrap: wrap;

		margin: var(--sp0) 0;
	}

	.line {
		padding-top: 16px;
	}
</style>
