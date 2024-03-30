<script>
	import { slide } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';
	import { module } from '$lib/store.js';

	import Button from '$lib/button.svelte';
	import Card from '$lib/card.svelte';
	import ButtonFold from '$lib/button.fold.svelte';
	import Check from '$lib/button.check.svelte';
	import Role_Ok from './role._ok.svelte';

	export let user;
	export let roles;
	let user_roles = [...user.roles];
	let open = true;

	const select_group = (_in) => {
		let group = [];
		for (const [name, r0les] of Object.entries(roles)) {
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
			if (!user_roles.includes(x)) {
				add_all = true;
				break;
			}
		}

		if (add_all) {
			for (const x of group) {
				if (!user_roles.includes(x)) {
					user_roles.push(x);
				}
			}
			user_roles = user_roles;
		} else {
			user_roles = user_roles.filter((x) => !group.includes(x));
		}
	};

	const select = (role) => {
		if (!user_roles.includes(role)) {
			user_roles.push(role);
			user_roles = user_roles;
		} else {
			user_roles = user_roles.filter((x) => x != role);
		}
	};
</script>

<Card>
	<div class="title">
		Roles
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

			{#each Object.entries(roles) as [name, r0les]}
				<span>
					<Button
						class="link small"
						on:click={() => {
							select_group(name);
						}}
					>
						{name}
					</Button>
				</span>

				{#each [1, 2, 3] as x}
					<span>
						{#each r0les as role}
							{#if role[1] == x}
								<Check
									active={user_roles.includes(`${name}:${role[0]}`)}
									on:click={() => {
										select(`${name}:${role[0]}`);
									}}
								>
									{role[0].split('_').join(' ')}
								</Check>
							{/if}
						{/each}
					</span>
				{/each}
			{/each}
		</section>

		<br />

		<Button
			class="primary"
			on:click={() => {
				$module = {
					module: Role_Ok,
					key: user.key,
					roles: user_roles
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
