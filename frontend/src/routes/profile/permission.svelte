<script>
	import { slide } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';
	import { module } from '$lib/store.js';

	import Button from '$lib/button.svelte';
	import Tag from '$lib/button.tag.svelte';
	import Card from '$lib/card.svelte';
	import ButtonFold from '$lib/button.fold.svelte';
	import Permission_Ok from './permission._ok.svelte';

	export let user;
	export let permissions;
	let permits = [...user.permissions];
	let init = [...user.permissions];
	let open = true;

	const select_group = (_in) => {
		let group = [];
		for (const [name, r0les] of Object.entries(permissions)) {
			for (const x of r0les) {
				if (_in == name) {
					group.push(`${name}:${x[0]}`);
				} else if (_in == x[1]) {
					group.push(`${name}:${x[0]}`);
				} else if (!_in) {
					group.push(`${name}:${x[0]}`);
				}
			}
		}

		let add_all = false;
		for (const x of group) {
			if (!permits.includes(x)) {
				add_all = true;
				break;
			}
		}

		if (add_all) {
			for (const x of group) {
				if (!permits.includes(x)) {
					permits.push(x);
				}
			}
			permits = permits;
		} else {
			permits = permits.filter((x) => !group.includes(x));
		}
	};

	const select = (_in) => {
		if (permits.includes(_in)) {
			permits = permits.filter((x) => x != _in);
		} else {
			permits.push(_in);
			permits = permits;
		}
	};

	let disabled = true;
	$: {
		let t1 = permits.sort((a, b) => a - b).join(',');
		let t2 = init.sort((a, b) => a - b).join(',');
		disabled = t1 == t2;
	}
</script>

<Card>
	<div class="title">
		Permissions
		<ButtonFold
			{open}
			on:click={() => {
				open = !open;
			}}
		/>
	</div>

	{#if open}
		<br />
		<section transition:slide|local={{ delay: 0, duration: 200, easing: cubicInOut }}>
			<span>
				<Button
					class="link small"
					on:click={() => {
						select_group();
					}}
				>
					category
				</Button>
			</span>

			{#each [1, 2, 3] as x}
				<span>
					<Button
						class="link small"
						on:click={() => {
							select_group(x);
						}}
					>
						Level {x}
					</Button>
				</span>
			{/each}

			{#each Object.entries(permissions) as [_type, _actions]}
				<span>
					<Button
						class="link small"
						on:click={() => {
							select_group(_type);
						}}
					>
						{_type}
					</Button>
				</span>

				{#each [1, 2, 3] as x}
					<span>
						{#each _actions as action}
							{#if action[1] == x}
								<!-- <Check
									active={permits.includes(`${_type}:${action[0]}`)}
									on:click={() => {
										select(`${_type}:${action[0]}`);
									}}
								>
									{action[0].split('_').join(' ')}
								</Check> -->

								<Tag
									active={permits.includes(`${_type}:${action[0]}`)}
									on:click={() => {
										select(`${_type}:${action[0]}`);
									}}
								>
									{action[0].split('_').join(' ')}
								</Tag>
							{/if}
						{/each}
					</span>
				{/each}
			{/each}
		</section>

		<br />

		<Button
			class="primary"
			{disabled}
			on:click={() => {
				$module = {
					module: Permission_Ok,
					key: user.key,
					permissions: permits
				};
			}}
		>
			Ok
		</Button>
	{/if}
</Card>

<style>
	.title {
		font-weight: 900;
		display: flex;
		justify-content: space-between;
		align-items: center;
	}

	section {
		display: grid;
		grid-template-columns: repeat(4, auto);
	}

	span {
		display: flex;
		flex-wrap: wrap;
		gap: var(--sp0);
		align-items: center;

		outline: 1px solid var(--ac4);
		padding: var(--sp0);
	}
</style>
