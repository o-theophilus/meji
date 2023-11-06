<script>
	import Button from '$lib/button.svelte';
	import Card from '$lib/card.svelte';
	import Center from '$lib/center.svelte';

	let roles = {
		admin: {
			level_1: ['dashboard'],
			level_2: ['manage_photo'],
			level_3: []
		},
		user: {
			level_1: ['view', 'view_all'],
			level_2: [],
			level_3: ['set permission']
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
	let user_roles = [];

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
</script>

<Center>
	<br />
	<div class="ctitle">Permission</div>
</Center>

<Card>
	<section>
		<span>
			<button
				class="role"
				on:click={() => {
					select_group();
				}}
			>
				category
			</button>
		</span>

		{#each ['level_1', 'level_2', 'level_3'] as level}
			<span>
				<button
					class="role"
					on:click={() => {
						select_group(level, 'level');
					}}
				>
					{level.split('_').join(' ')}
				</button>
			</span>
		{/each}

		{#each Object.entries(roles) as [cate, levels]}
			<span>
				<button
					class="role"
					on:click={() => {
						select_group(cate, 'cate');
					}}
				>
					{cate}
				</button>
			</span>
			{#each Object.entries(levels) as [level, roles]}
				<span>
					{#each roles as role}
						<button
							class="role"
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
	<Button class="primary">Ok</Button>
</Card>

<style>
	section {
		display: grid;
		grid-template-columns: repeat(4, auto);
		font-size: small;
	}

	span {
		display: flex;
		flex-wrap: wrap;
		gap: var(--sp0);
		align-items: center;

		outline: 1px solid var(--ac4);
		padding: var(--sp1);
	}

	.role {
		padding: var(--sp0);
		border-radius: var(--sp0);
		background-color: var(--ac5);
		color: var(--ac2);
		border: none;

		cursor: pointer;
	}
	.role:hover {
		background-color: var(--ac4);
	}
	.active {
		background-color: var(--cl1);
		color: var(--ac6_);
	}
	/* button {
		width: 20px;
		aspect-ratio: 1/1;
	} */
</style>
