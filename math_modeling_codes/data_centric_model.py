import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset, random_split
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Synthesize data
np.random.seed(42)

# Generate synthetic features
temperature = np.random.uniform(10, 25, 1000)  # temperature in degrees Celsius
nutrients = np.random.uniform(0.5, 5, 1000)    # nutrient concentration in mg/L
light = np.random.uniform(100, 1000, 1000)     # light intensity in µmol/m^2/s

# Generate synthetic outputs based on assumed relationships
algae_growth_rate = 0.1 * temperature + 0.5 * nutrients + 0.01 * light + np.random.normal(0, 0.5, 1000)
mussel_feeding_rate = 0.2 * temperature + 0.3 * nutrients + 0.005 * light + np.random.normal(0, 0.5, 1000)

# Create a DataFrame
data = pd.DataFrame({
    'temperature': temperature,
    'nutrients': nutrients,
    'light': light,
    'algae_growth_rate': algae_growth_rate,
    'mussel_feeding_rate': mussel_feeding_rate
})

data.to_csv('synthetic_data.csv', index=False)
# data = pd.read_csv('/Users/luoyaxin/Desktop/db4/Synthetic_Data_for_Algae_Growth_and_Mussel_Feeding_Rates.csv')

# Feature columns
features = ['temperature', 'nutrients', 'light']
X = data[features].values
y = data[['algae_growth_rate', 'mussel_feeding_rate']].values

# Normalize data
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X = scaler.fit_transform(X)

# # Pairplot to visualize relationships between variables
# sns.pairplot(data)
# plt.suptitle('Pairplot of Features and Targets', y=1.02)
# plt.show()

# # Visualize the relationships between each feature and the targets
# fig, axes = plt.subplots(3, 2, figsize=(14, 12))
# fig.suptitle('Relationships between Features and Targets')

# features = ['temperature', 'nutrients', 'light']
# targets = ['algae_growth_rate', 'mussel_feeding_rate']

# for i, feature in enumerate(features):
#     for j, target in enumerate(targets):
#         sns.scatterplot(ax=axes[i, j], x=data[feature], y=data[target])
#         axes[i, j].set_title(f'{feature} vs {target}')
#         axes[i, j].set_xlabel(feature)
#         axes[i, j].set_ylabel(target)

# plt.tight_layout(rect=[0, 0, 1, 0.96])
# plt.show()
# exit()
# Visualize Temperature vs Mussel Feeding Rate
plt.figure(figsize=(8, 6))
sns.scatterplot(x=data['temperature'], y=data['mussel_feeding_rate'])
plt.title('Temperature vs Mussel Feeding Rate')
plt.xlabel('Temperature (°C)')
plt.ylabel('Mussel Feeding Rate')
plt.grid(True)
plt.show()

# Visualize Nutrients vs Mussel Feeding Rate
plt.figure(figsize=(8, 6))
sns.scatterplot(x=data['nutrients'], y=data['mussel_feeding_rate'])
plt.title('Nutrients vs Mussel Feeding Rate')
plt.xlabel('Nutrients (mg/L)')
plt.ylabel('Mussel Feeding Rate')
plt.grid(True)
plt.show()

# Visualize Light vs Algae Growth Rate
plt.figure(figsize=(8, 6))
sns.scatterplot(x=data['light'], y=data['algae_growth_rate'])
plt.title('Light vs Algae Growth Rate')
plt.xlabel('Light (µmol/m^2/s)')
plt.ylabel('Algae Growth Rate')
plt.grid(True)
plt.show()
exit()
# Convert to PyTorch tensors
X = torch.tensor(X, dtype=torch.float32)
y = torch.tensor(y, dtype=torch.float32)

# Create a Dataset
class AlgaeMusselDataset(Dataset):
    def __init__(self, X, y):
        self.X = X
        self.y = y
    
    def __len__(self):
        return len(self.X)
    
    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]

dataset = AlgaeMusselDataset(X, y)

# Split into training and test sets
train_size = int(0.8 * len(dataset))
test_size = len(dataset) - train_size
train_dataset, test_dataset = random_split(dataset, [train_size, test_size])

# Create DataLoaders
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)


class AlgaeMusselNN(nn.Module):
    def __init__(self):
        super(AlgaeMusselNN, self).__init__()
        self.fc1 = nn.Linear(3, 64)
        self.fc2 = nn.Linear(64, 64)
        self.fc3 = nn.Linear(64, 2)  # Output layer for two predictions
    
    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x

model = AlgaeMusselNN()


# Define loss function and optimizer
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training loop
num_epochs = 1000

for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0
    for inputs, targets in train_loader:
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, targets)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()
    
    print(f'Epoch {epoch+1}/{num_epochs}, Loss: {running_loss/len(train_loader)}')
model.eval()
test_loss = 0.0
with torch.no_grad():
    for inputs, targets in test_loader:
        outputs = model(inputs)
        loss = criterion(outputs, targets)
        test_loss += loss.item()

print(f'Test Loss: {test_loss/len(test_loader)}')
