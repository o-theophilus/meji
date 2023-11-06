<script>
	import { slide } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';
	import { user as me, toast, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/button.svelte';
	import Card from '$lib/card.svelte';
	import ButtonFold from '$lib/button.fold.svelte';

	export let user;
	let user_roles = [...user.roles];
	let open = true;
	let error = {};

	let roles = {
		admin: {
			level_1: ['dashboard'],
			level_2: ['manage_photo'],
			level_3: []
		},
		user: {
			level_1: ['view', 'view_all'],
			level_2: ['view_balance'],
			level_3: ['set_permission']
		},
		item: {
			level_1: [],
			level_2: ['add', 'edit', 'advert', 'change_status'],
			level_3: []
		},
		voucher: {
			level_1: ['view', 'view_all'],
			level_2: [],
			level_3: ['add', 'view_code']
		},
		log: {
			level_1: ['view'],
			level_2: [],
			level_3: []
		}
	};

	const select_group = (_in = '', _group = '') => {
		let group = [];
		for (const [_cate, _levels] of Object.entries(roles)) {
			for (const [_level, _roles] of Object.entries(_levels)) {
				if (_group == 'level' && _level == _in) {
					for (const _role of _roles) {
						group.push(`${_cate}:${_role}`);
					}
				} else if (_group == 'cate' && _cate == _in) {
					for (const _role of _roles) {
						group.push(`${_cate}:${_role}`);
					}
				} else if (!_group && !_in) {
					for (const _role of _roles) {
						group.push(`${_cate}:${_role}`);
					}
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
			user_roles = [...user_roles, ...group];
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

	const submit = async () => {
		$loading = 'saving . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user_role/${user.key}`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({ roles: user_roles })
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			$toast = {
				status: 200,
				message: 'Role saved'
			};
		} else {
			error = resp;
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

			{#each ['level_1', 'level_2', 'level_3'] as level}
				<span>
					<Button
						class="link small"
						on:click={() => {
							select_group(level, 'level');
						}}
					>
						{level.split('_').join(' ')}
					</Button>
				</span>
			{/each}

			{#each Object.entries(roles) as [cate, levels]}
				<span>
					<Button
						class="link small"
						on:click={() => {
							select_group(cate, 'cate');
						}}
					>
						{cate}
					</Button>
				</span>
				{#each Object.entries(levels) as [level, roles]}
					<span>
						{#each roles as role}
							<button
								class:active={user_roles.includes(`${cate}:${role}`)}
								on:click={() => {
									select(`${cate}:${role}`);
								}}
							>
								{role.split('_').join(' ')}
							</button>
						{/each}
					</span>
				{/each}
			{/each}
		</section>

		<br />
		{#if error.error}
			<p class="error">
				{error.error}
			</p>
			<br />
		{/if}

		<Button class="primary" on:click={submit}>Ok</Button>
	{/if}
</Card>

<style>
	.title {
		font-weight: 600;
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
		padding: var(--sp1);
	}

	button {
		padding: var(--sp0);
		border-radius: var(--sp0);
		background-color: var(--ac5);
		color: var(--ac2);
		border: none;
		font-size: small;

		cursor: pointer;
	}
	button.active {
		color: var(--ac6_);
		background-color: var(--cl1);
	}
	button:hover {
		color: var(--ac6_);
		background-color: var(--cl2);
	}
</style>
